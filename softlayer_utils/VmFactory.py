import argparse
import Client
import json
import SoftLayer
import sys

class VmFactory:
    """
    A utility class to create virtual machines.

    instance variables:
        verbose - current flag setting for verbose logging
    """
    def __init__(self):
        self.verbose = False

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
    
    def create_default_vm(self, client, hostname, domain="fcc-atlas-project.net"):
        vGuestObject = client['Virtual_Guest'] 
        #verifyOrderObject= client['Product_Order'] 

        creation = vGuestObject.createObject(
            {
                "hostname"                     : hostname,
                "domain"                       : domain,
                "startCpus"                    : "1",
                "maxMemory"                    : "4096",
                "hourlyBillingFlag"            : True,
                "datacenter"                   : { "name": "dal05" },
                "operatingSystemReferenceCode" : "CENTOS_6_64",
                "localDiskFlag"                : False,
                "sshKeys"                      : [ { "id": 115146 } ] 
            }
        ) 

        print "order details:\n{0}".format(json.dumps(creation, indent=4)) 

    # Parse the command line arguments via argparse.ArgumentParser.
    # 
    # Run with --help to view description of valid arguments.
    #
    # arg: args - list of the command line arguments
    # Return value: the args dict returned from parser.parse_args(args)
    def parse_command_line(self, args):
        parser = argparse.ArgumentParser(description='Altas FCC Context Switching Tool')
        parser.add_argument("client", help="the client (or user) to whom the new virtual machine will be attributed")
        parser.add_argument("hostname", help="the desired hostname for the new virtual machine")
        parser.add_argument("--domain", help="the domain to which the host will be added", default="fcc-atlas-project.net")
        parser.add_argument("--verbose", "-v", action="store_true", help="log actions to the console")
        return parser.parse_args(args)

    # Invoke the context-switch algorithm with the specified command-line arguments
    # 
    # arg: args - the command line arguments from sys.argv
    # Return value - None    
    def create_vm(self, args):
        args = self.parse_command_line(args)
        self.set_verbosity(args)
   
        client = Client.get_client(args.client)
        self.create_default_vm(client, args.hostname, args.domain)

if __name__ == '__main__':
    process_args = sys.argv[1:] # get the command line arguments excluding the class name
    switcher = VmFactory()
    switcher.create_vm(process_args)