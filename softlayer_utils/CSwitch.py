import argparse
import os
import shutil
import subprocess
import time
import sys

class CSwitch:
    """
    A utility class for swapping SSH key-pairs between different contexts
    in order to seamlessly be able to switch development environments between:
    dev, demo, int, prod and local

    instance variables:
        DOES_EXIST - flag indicated a search should check for path existence
        DOES_NOT_EXIST - flag indicated a search should check for path availability
        DIRECTORIES - list of direct subdirectories expected to exist in the context root directory
        CONTEXTS - list of named environment contexts
        verbose - current flag setting for verbose logging
        script_file - current named file for the script to generate the context's key-pairs
    """
    def __init__(self):
        self.DOES_EXIST = True
        self.DOES_NOT_EXIST = False
        self.DIRECTORIES = ['archived', 'local', 'atlas']
        self.CONTEXTS = ['dev', 'int', 'demo', 'prod']

        self.verbose = False
        self.script_file = 'create-key-pair.sh'
    

    # Log a message
    #
    # arg: message - the message to be logged
    # arg: force - whether the message should be logged regardless of the verbosity flag
    #         True will ignore the verbosity flag
    #         False will abide by the verbosity flag
    # return value: None
    def log(self, message, force=False):
        if self.verbose or force:
            print message
    
    # Return the verbosity of the output
    #
    # Return value: True or False 
    def is_verbose(self):
        return self.verbose
    
    # Set the verbosity of the output based on the specified dict
    #
    # arg: args - the args dict created by argparse and expected to contain an args.verbose
    # Return value: True or False
    # TODO: check for dict or accept only a boolean
    def set_verbosity(self, args):
        if args.verbose:
            self.verbose = True
            
    # Set the script file to be invoked to the specified file name.  
    #
    # arg: filename - the name of the file to invoke from the current 
    #      working directory
    # Return value: None
    # TODO: check for dict or accept only a boolean
    def set_script_file(self, filename):
        self.script_file = filename
        
    # Get the name of the script file to invoke from the current working directory.
    #
    # Return value: the name of the file to be invoked
    def get_script_file(self):
        return self.script_file
    
    # Verify the existence of a directory
    #
    # arg: type - a description of the type of path - for logging
    # arg: path - the path to the file or directory
    # arg: exists - whether it should check for existence or non-existence
    #        True will verify the path exists
    #        False will verify the path does NOT exist
    # Return value: True - if 'exists' is True and the path exists or if 'exists'
    #                      is False and the path does not exist
    #               False - if 'exists' is True and the path does not exist or
    #                       if 'exists' is False and the path does exist
    def verify_existence(self, pathType, path, exists=False):
        retVal = True
        if exists == self.DOES_EXIST:
            if not os.path.exists(path):
                self.log("{0} {1} does not exist".format(pathType, path), True)
                #exit(1)
                retVal = False
        else:
            if os.path.exists(path):
                self.log("{0} {1} exists already".format(pathType, path), True)
                #exit(1)
                retVal = False
        return retVal
    
    # Create the directory path to the script in the current working directory
    #
    # Return value: a path to the class' script file in the current working directory
    def get_script_path(self): 
        return os.path.join(os.getcwd(), self.script_file)
    
    # Get the path that will contain the various context key-pairs.  Will return
    # the .ssh directory under the system's home directory if it is not specified
    # in the arguments.
    #
    # arg: args - the args dict created by argparse and expected to contain an args.dir
    # Return value: the value of args.dir or the path to the user's {home}/.ssh directory
    def get_root_dir(self, args): 
        if args.dir:
            rootPath = args.dir
        else:
            rootPath = os.path.join(os.environ['HOME'], '.ssh')
        #verify_existence('SSH root directory', rootPath, self.DOES_EXIST)
        return rootPath

    # Get the path for the specified context.
    #
    # arg: path - the root directory containing the various context directories
    # arg: context - the type of context the path should represent
    # Return value: the path to the specified context directory.      
    def get_context_dir(self, path, context): 
        if context == 'local':
            contextPath = os.path.join(path, context)
        else:
            contextPath = os.path.join(path, 'atlas', context)
        return contextPath
    
    # Create an archive of the existing keys in order to perform non-destructive 
    # operations.
    #
    # arg: path - the path of the directory that is to be archived
    # Return value: None 
    def archive_files(self, path):
        # create the 'archived' directory if one does not already exist
        archivePath = os.path.join(path, "archived")
        if not os.path.exists(archivePath):
            os.mkdir(archivePath)
            self.log("created directory: {0}".format(archivePath))
    
        # create a time-stamped acrhived subdirectory
        # the path should NOt already exist, so just exit-out if it does
        archiveDir = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        archivePath = os.path.join(path, "archived", archiveDir)
        if os.path.exists(archivePath):
            self.log("{0} archive path already exists - cannot proceeed".format(archivePath), True)
            exit(1)
        else:
            os.mkdir(archivePath)
            self.log("created directory: {0}".format(archivePath))
    
        # get a list of files and directories that are in directory to be archived
        # move each file and directory in the list to the archive directory
        names = os.listdir(path)
        for name in names:
            filePath = os.path.join(path, name)
            if os.path.isfile(filePath):
                shutil.move(filePath, archivePath)
                self.log("archived file {0} from {1} to {2}".format(name, path, archivePath))
    
    # Clone the files in the specified context path to the root path
    #
    # arg: rootPath - the path to the directory to receive the key-pairs for the specified context
    # arg: contextPath - the path to the directory containing the desired context key-pairs
    # Return value: None
    def clone_context_files(self, rootPath, contextPath):
        # get a list of files and directories that are in context directory to be cloned
        # move each file and directory in the list to the archive directory
        names = os.listdir(contextPath)
        for name in names:
            filePath = os.path.join(os.path.abspath(contextPath), name)
            shutil.copy2(filePath, rootPath)
            self.log("cloned file {0} from {1} to {2}".format(name, contextPath, rootPath))
    
    # Create a set of keys in the specified directory.  The script will generate
    # default RSA id_rsa and id_rsa.pub private and public keys, respectively, as
    # well as an id_rsa.key-pair.context descriptor file where 'context' is the
    # name of the context associated with the specified keyPath.
    #
    # arg: keyPath - the directory path for the intended key-pair files
    # Return value: None
    #
    # Executing the script contents within python with subprocess will yield the following results:
    #     - subprocess.call(cmd, shell=False) -> gives an error for the password being too short
    #     - subprocess.call(cmd, shell=True) -> prompts user for directory to create the file despite
    #           the -f argument in the command line         
    def create_key(self, keyPath):
        descriptor = os.path.split(keyPath)[1]
        command = "{0} {1} {2} {3}".format(self.get_script_path(), keyPath, descriptor, self.verbose)
        subprocess.call(command, shell=True)
        
    # Generate a list of paths based on the associated context types
    #
    # arg: rootPath - the root directory for the context paths
    # Return value: a list of paths associated with the different contexts
    def get_paths_to_create(self, rootPath):
        paths = [ ]
        # append to the list each of the primary subdirectories
        for subpath in self.DIRECTORIES:
            path = os.path.join(rootPath, subpath) 
            paths.append(path)
        # append to the list each of the associated contexts for the atlas environments
        for context in self.CONTEXTS:
            path = os.path.join(rootPath, 'atlas', context) 
            paths.append(path)
        return paths    
        
    # Verify the specified directory path has not existing directory paths that
    # might conflict with the paths expected to be generated
    #
    # arg: rootPath - the path to be inspected 
    # Return value: True if there are no conflicting paths that already exist, 
    #               False otherwise
    def verify_target_dir_is_available(self, rootPath):
        retVal = False
        # get the paths to verify
        paths_to_verify = self.get_paths_to_create(rootPath)   
        # verify each path - breaking the loop once one is found     
        for path_to_verify in paths_to_verify:
            if self.verify_existence('initialization directory', path_to_verify, self.DOES_NOT_EXIST) == False:
                break        
        else:
            retVal = True
        return retVal    

    # Create the set of context paths and key-pairs for each context
    #
    # arg: paths - the list of paths to receive an auto-generated key-pair
    # Return value - an error string if one was generated, or None otherwise
    def create_initial_contexts(self, paths):
        retValError = None
        if isinstance(paths, list):
            for path in paths:
                try:
                    os.makedirs(path)                    
                    lastDir = os.path.split(path)[1]
                    if lastDir != 'archived' and lastDir != 'atlas':
                        self.create_key(path)
                        self.log("created directory: {0}".format(path))
                except OSError as ose:
                    if ose.errno == 17: # path already exists
                        retValError = 'directory exists and therefore is not available'
                    else: 
                        retValError = '{0}: {1}'.format('unexpected OSError: ', str(ose))
                except Exception as e: 
                    retValError = '{0}: {1}'.format('unexpected exception: ', str(e))
        else:
            retValError = 'paths argument is not a list'
        return retValError
            
    # Initialize the different contexts in the specified root directory
    #
    # arg: rootPath - the path to the root directory to contain the context directories
    # arg: initial_context - the initial context to be configued in the root path
    # Return value: None
    # Exceptions: BaseException - when the rootPath already exists or the 
    #                             script_path file does not exist
    def initialize_contexts(self, rootPath, initial_context):
        dir_is_available = self.verify_target_dir_is_available(rootPath) 
        key_generation_script_exists = self.verify_existence('rsa key generator', self.get_script_path(), self.DOES_EXIST)
        
        if (dir_is_available == False):
            raise BaseException('directory exists and therefore is not available')
        elif (key_generation_script_exists == False):
            raise BaseException('cannot find key generation script')
        else:
            # get the context paths to create, create the initial contexts and
            # configure the setup for the specified initial context
            paths = self.get_paths_to_create(rootPath)
            self.create_initial_contexts(paths)
            self.switch_contexts(rootPath, initial_context, False)
    
    # Switch the active context to the specified context
    #
    # arg: rootPath - the root directory containing the contexts
    # arg: context - the context to be activated
    # arg: do_archive - flag indicating whether the existing context or keys
    #                   should be archived; True (default) will archive the
    #                   existing keys, False will skip archiving
    # TODO: verify do_archive=False deletes the files and does not leave
    #       files unintentionally behind (probably just the id_rsa.key-pairs.context 
    #       identifier file would be left behind, but then there would be two
    #       and it could be ambigous without looking at the timestamps on the files
    def switch_contexts(self, rootPath, context, do_archive=True):
        contextPath = self.get_context_dir(rootPath, context)
        if do_archive:
            self.archive_files(rootPath)
        self.clone_context_files(rootPath, contextPath)
    
    # Parse the command line arguments via argparse.ArgumentParser.
    # 
    # Run with --help to view description of valid arguments.
    #
    # arg: args - list of the command line arguments
    # Return value: the args dict returned from parser.parse_args(args)
    def parse_command_line(self, args):
        parser = argparse.ArgumentParser(description='Altas FCC Context Switching Tool')
        parser.add_argument("--dir", help="root directory containing the atlas context sub-directories")
        parser.add_argument("--verbose", "-v", action="store_true", help="log actions to the console")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--context", choices=["local", "dev", "demo", "int", "prod"], help="which context to install")
        group.add_argument("--init", choices=["local", "dev", "demo", "int", "prod"], help="initialize the context directory structure with specified context")
        return parser.parse_args(args)

    # Invoke the context-switch algorithm with the specified command-line arguments
    # 
    # arg: args - the command line arguments from sys.argv
    # Return value - None    
    def perform_switch(self, args):
        args = self.parse_command_line(args)
        self.set_verbosity(args)
        rootPath = self.get_root_dir(args)
   
        if args.init:
            self.initialize_contexts(rootPath, args.init)
        else:
            self.switch_contexts(rootPath, args.context, True)

if __name__ == '__main__':
    process_args = sys.argv[1:] # get the command line arguments excluding the class name
    switcher = CSwitch()
    switcher.perform_switch(process_args)