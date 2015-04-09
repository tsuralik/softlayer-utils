from CSwitch import CSwitch
import os
import shutil
import time
import unittest

class TestCSwitch(unittest.TestCase):
    
    testDir = '/tmp/cSwitch'

    @classmethod
    def setUpClass(cls):
        super(TestCSwitch, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestCSwitch, cls).tearDownClass()

    def setUp(self):
        self.cswitch = CSwitch()
        print "instance: ", self.cswitch
        
        if os.path.exists(TestCSwitch.testDir):
            os.rmdir(TestCSwitch.testDir)

    def tearDown(self):
        if os.path.exists(TestCSwitch.testDir):
            #os.rmdir(TestCSwitch.testDir)
            shutil.rmtree(TestCSwitch.testDir)
        self.cswitch = None
            
    def test_verify_existence_path_exists_when_it_does_exist(self):
        self.assertFalse(os.path.exists(TestCSwitch.testDir))
        # make the directory for this test case
        os.mkdir(TestCSwitch.testDir)
        retVal = self.cswitch.verify_existence('unittest', TestCSwitch.testDir, True)
        self.assertEquals(retVal, True)
        
    def test_verify_existence_path_exists_when_it_does_not_exist(self):
        self.assertFalse(os.path.exists(TestCSwitch.testDir))
        retVal = self.cswitch.verify_existence('unittest', TestCSwitch.testDir, True)
        self.assertEquals(retVal, False)
            
    def test_verify_existence_path_does_not_exist_when_it_does_exist(self):
        # make the directory for this test case
        os.mkdir(TestCSwitch.testDir)
        retVal = self.cswitch.verify_existence('unittest', TestCSwitch.testDir, False)
        self.assertEquals(retVal, False)
            
    def test_verify_existence_path_does_not_exist_when_it_does_not_exist(self):
        retVal = self.cswitch.verify_existence('unittest', TestCSwitch.testDir, False)
        self.assertEquals(retVal, True)
        
    #def test_script_path_creation(self):
    #    retVal = CSwitch.get_script_path()
    #    self.assertEquals(os.path.join(os.getcwd(), 'create-key-pair.sh'), retVal)
        
    def test_args_with_verbosity(self):
        args = self.cswitch.parse_command_line(['--dir', '/tmp/cSwitch', '--init', 'demo', '--verbose'])
        self.assertTrue(args.verbose)
        
    def test_args_without_verbosity(self):
        args = self.cswitch.parse_command_line(['--dir', '/tmp/cSwitch', '--init', 'demo'])
        self.assertFalse(args.verbose)
        
    def test_args_set_verbosity_with_args(self):
        args = self.cswitch.parse_command_line(['--dir', '/tmp/cSwitch', '--init', 'demo', '--verbose'])
        self.cswitch.set_verbosity(args)
        self.assertTrue(self.cswitch.is_verbose())
        
    def test_args_get_root_dir_with_dir_arg(self):
        args = self.cswitch.parse_command_line(['--dir', '/tmp/cSwitch', '--init', 'demo', '--verbose'])
        actual_root_dir = self.cswitch.get_root_dir(args)
        self.assertEquals(actual_root_dir, '/tmp/cSwitch')
        
    def test_args_get_root_dir_without_dir_arg(self):
        args = self.cswitch.parse_command_line(['--init', 'demo', '--verbose'])
        expected_root_dir = os.path.join(os.environ['HOME'], '.ssh')
        actual_root_dir = self.cswitch.get_root_dir(args)
        self.assertEquals(actual_root_dir, expected_root_dir)
        
    def test_get_context_directory_for_local(self):
        context_path = self.cswitch.get_context_dir('/testPath', 'local')
        self.assertEquals(context_path, '/testPath/local')
        
    def test_get_context_directory_for_demo(self):
        context_path = self.cswitch.get_context_dir('/testPath', 'demo')
        self.assertEquals(context_path, '/testPath/atlas/demo')
        
    def test_get_context_directory_for_dev(self):
        context_path = self.cswitch.get_context_dir('/testPath', 'dev')
        self.assertEquals(context_path, '/testPath/atlas/dev')
        
    def test_get_context_directory_for_int(self):
        context_path = self.cswitch.get_context_dir('/testPath', 'int')
        self.assertEquals(context_path, '/testPath/atlas/int')
        
    def test_get_context_directory_for_prod(self):
        context_path = self.cswitch.get_context_dir('/testPath', 'prod')
        self.assertEquals(context_path, '/testPath/atlas/prod')
        
    def test_target_dir_is_available(self):
        available = self.cswitch.verify_target_dir_is_available('/tmp/cSwitch')
        self.assertTrue(available)
        
    def test_target_dir_is_not_available_due_to_archived(self):
        # make the directory for this test case
        os.mkdir(TestCSwitch.testDir)
        os.mkdir(os.path.join(TestCSwitch.testDir, 'archived'))        
        available = self.cswitch.verify_target_dir_is_available(TestCSwitch.testDir)
        self.assertFalse(available)
        
    def test_target_dir_is_not_available_due_to_local(self):
        # make the directory for this test case
        os.mkdir(TestCSwitch.testDir)
        os.mkdir(os.path.join(TestCSwitch.testDir, 'local'))        
        available = self.cswitch.verify_target_dir_is_available(TestCSwitch.testDir)
        self.assertFalse(available)
        
    def test_target_dir_is_not_available_due_to_atlas(self):
        # make the directory for this test case
        os.mkdir(TestCSwitch.testDir)
        os.mkdir(os.path.join(TestCSwitch.testDir, 'atlas'))        
        available = self.cswitch.verify_target_dir_is_available(TestCSwitch.testDir)
        self.assertFalse(available)
        
    def test_get_paths_to_create_has_archived(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.assertIn(os.path.join(TestCSwitch.testDir, 'archived'), paths)
        
    def test_get_paths_to_create_has_local(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.assertIn(os.path.join(TestCSwitch.testDir, 'local'), paths)
        
    def test_get_paths_to_create_has_demo(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.assertIn(os.path.join(TestCSwitch.testDir, 'atlas', 'demo'), paths)
        
    def test_get_paths_to_create_has_dev(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.assertIn(os.path.join(TestCSwitch.testDir, 'atlas', 'dev'), paths)
        
    def test_get_paths_to_create_has_int(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.assertIn(os.path.join(TestCSwitch.testDir, 'atlas', 'int'), paths)
        
    def test_get_paths_to_create_has_prod(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.assertIn(os.path.join(TestCSwitch.testDir, 'atlas', 'prod'), paths)
    
    def test_creates_initial_directory_archived(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.cswitch.create_initial_contexts(paths)
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'archived')))    
    
    def test_creates_initial_directory_local(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.cswitch.create_initial_contexts(paths)
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'local')))    
        #time.sleep(1) 
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'local', 'id_rsa')))   
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'local', 'id_rsa.pub')))   
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'local', 'id_rsa.key-pair.local')))   
    
    def test_creates_initial_directory_atlas(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.cswitch.create_initial_contexts(paths)
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas')))    
    
    def test_creates_initial_directory_dev(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.cswitch.create_initial_contexts(paths)
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'dev')))     
        #time.sleep(1) 
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'dev', 'id_rsa')))   
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'dev', 'id_rsa.pub')))   
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'dev', 'id_rsa.key-pair.dev')))     
    
    def test_creates_initial_directory_demo(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.cswitch.create_initial_contexts(paths)
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'demo')))     
        #time.sleep(1) 
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'demo', 'id_rsa')))   
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'demo', 'id_rsa.pub')))   
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'demo', 'id_rsa.key-pair.demo')))     
    
    def test_creates_initial_directory_int(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.cswitch.create_initial_contexts(paths)
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'int')))       
        #time.sleep(1) 
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'int', 'id_rsa')))   
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'int', 'id_rsa.pub')))   
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'int', 'id_rsa.key-pair.int')))   
    
    def test_creates_initial_directory_prod(self):
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        self.cswitch.create_initial_contexts(paths)
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'prod')))  
        #time.sleep(1) 
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'prod', 'id_rsa')))   
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'prod', 'id_rsa.pub')))   
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'prod', 'id_rsa.key-pair.prod')))   
    
    def test_creates_initial_directory_with_non_list(self):
        retVal = self.cswitch.create_initial_contexts('foo')
        self.assertEquals(retVal, 'paths argument is not a list')
            
    def test_create_initial_contexts_throws_unknown_oserror(self):
        paths = [ ['foo', 'bar'], ['baz'] ]
        retVal = self.cswitch.create_initial_contexts(paths)
        print retVal
        time.sleep(15)
        self.assertTrue(retVal.startswith('unexpected exception:'))
            
    def test_create_initial_contexts_throws_directory_exists_exception(self):
        os.makedirs(os.path.join(TestCSwitch.testDir, 'atlas', 'prod'))
        paths = self.cswitch.get_paths_to_create(TestCSwitch.testDir)
        retVal = self.cswitch.create_initial_contexts(paths)
        self.assertEquals(retVal, 'directory exists and therefore is not available')
            
    def test_set_test_script(self):
        testname = 'foobar.sh'
        self.cswitch.set_script_file(testname)
        retValTestName = self.cswitch.get_script_file()
        self.assertEqual(retValTestName, testname)
        # TODO - get rid of this
        self.cswitch.set_script_file('create-key-pair.sh')
            
    def test_get_test_script(self):
        retValTestName = self.cswitch.get_script_file()
        self.assertEqual(retValTestName, 'create-key-pair.sh')        
            
    def test_initialize_contexts_when_missing_script_file(self):
        try:
            self.cswitch.set_script_file('foobar.sh')
            self.cswitch.initialize_contexts(TestCSwitch.testDir, 'local')
        except BaseException as be:
            self.assertEquals(be.message, 'cannot find key generation script')
        else:
            self.fail('should have failed to find script file')  
            
    def test_initialize_contexts_when_root_path_already_exists(self):
        os.makedirs(os.path.join(TestCSwitch.testDir, 'local'))
        try:
            self.cswitch.initialize_contexts(TestCSwitch.testDir, 'local')
        except BaseException as be:
            self.assertEquals(be.message, 'directory exists and therefore is not available')
        else:
            self.fail("expected a BaseException for a directory already existing") 
        
    def test_atlas_directory_does_not_get_key_pairs(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'local')
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas')))
        self.assertFalse(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'id_rsa')))
        self.assertFalse(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'id_rsa.pub')))
        self.assertFalse(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'id_rsa.key-pair.atlas')))

    def test_initialize_contexts_with_context_for_default_local(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'local')
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'local')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'archived')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'dev')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'demo')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'int')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'prod')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa.pub')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa.key-pair.local')))

    def test_initialize_contexts_with_context_for_dev(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'dev')
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'local')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'archived')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'dev')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'demo')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'int')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'prod')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa.pub')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa.key-pair.dev')))

    def test_initialize_contexts_with_context_for_demo(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'demo')
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'local')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'archived')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'dev')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'demo')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'int')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'prod')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa.pub')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa.key-pair.demo')))

    def test_initialize_contexts_with_context_for_int(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'int')
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'local')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'archived')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'dev')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'demo')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'int')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'prod')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa.pub')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa.key-pair.int')))

    def test_initialize_contexts_with_context_for_prod(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'prod')
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'local')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'archived')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'dev')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'demo')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'int')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'atlas', 'prod')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa.pub')))
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'id_rsa.key-pair.prod')))

    def test_initialize_contexts_does_not_get_archive_keys(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'prod')
        self.assertTrue(os.path.exists(os.path.join(TestCSwitch.testDir, 'archived')))
        self.assertFalse(os.path.exists(os.path.join(TestCSwitch.testDir, 'archived', 'id_rsa')))
        self.assertFalse(os.path.exists(os.path.join(TestCSwitch.testDir, 'archived', 'id_rsa.pub')))
        self.assertFalse(os.path.exists(os.path.join(TestCSwitch.testDir, 'archived', 'id_rsa.key-pair.archived')))

    def test_initialize_contexts_with_context_without_archiving(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'local')
        path = os.path.join(TestCSwitch.testDir, 'archived')
        self.assertEquals(len(os.listdir(path)), 0)
        
    def test_switch_contexts_with_archiving_from_initial_local_to_dev(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'local')
        self.cswitch.switch_contexts(TestCSwitch.testDir, 'dev', True)
        archivePath = os.path.join(TestCSwitch.testDir, 'archived')
        self.assertEquals(len(os.listdir(archivePath)), 1)
        timeStampedDir = os.listdir(archivePath)[0]
        timeStampedPath = os.path.join(archivePath, timeStampedDir)
        self.assertEquals(len(os.listdir(timeStampedPath)), 3)
        self.assertTrue(os.path.exists(os.path.join(timeStampedPath, 'id_rsa')))
        self.assertTrue(os.path.exists(os.path.join(timeStampedPath, 'id_rsa.pub')))
        self.assertTrue(os.path.exists(os.path.join(timeStampedPath, 'id_rsa.key-pair.local')))
        
    def test_switch_contexts_without_archiving_has_no_archive_dirs(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'local')
        self.cswitch.switch_contexts(TestCSwitch.testDir, 'dev', False)
        archivePath = os.path.join(TestCSwitch.testDir, 'archived')
        self.assertEquals(len(os.listdir(archivePath)), 0)
        
    def test_switch_contexts_after_the_archive_dir_was_deleted(self):
        self.cswitch.set_script_file('create-key-pair.sh')
        self.cswitch.initialize_contexts(TestCSwitch.testDir, 'local')
        archivePath = os.path.join(TestCSwitch.testDir, 'archived')
        shutil.rmtree(archivePath)
        self.assertFalse(os.path.exists(archivePath))
        self.cswitch.switch_contexts(TestCSwitch.testDir, 'dev', True)
        
        self.assertTrue(os.path.exists(archivePath))
        self.assertEquals(len(os.listdir(archivePath)), 1)
        timeStampedDir = os.listdir(archivePath)[0]
        timeStampedPath = os.path.join(archivePath, timeStampedDir)
        self.assertEquals(len(os.listdir(timeStampedPath)), 3)
        self.assertTrue(os.path.exists(os.path.join(timeStampedPath, 'id_rsa')))
        self.assertTrue(os.path.exists(os.path.join(timeStampedPath, 'id_rsa.pub')))
        self.assertTrue(os.path.exists(os.path.join(timeStampedPath, 'id_rsa.key-pair.local')))
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCSwitch))
    return suite
  
if __name__ == '__main__':
    unittest.main()