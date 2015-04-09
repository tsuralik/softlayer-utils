import unittest
import test_Account
import test_CSwitch 
    
#class TestAllTests(unittest.TestCase):
#    @classmethod
#    def setUpClass(cls):
#        super(TestAllTests, cls).setUpClass()

#    @classmethod
#    def tearDownClass(cls):
#        super(TestAllTests, cls).tearDownClass()
 
def suite():
    print "suiting"
    suites = [ ]
    suites.append(test_CSwitch.suite())
    suites.append(test_Account.suite())
    
    suite = unittest.TestSuite()

    alltests = unittest.TestSuite()
    for suite in suites:
        alltests.addTests(suite)
        
    return alltests
    
if __name__ == '__main__':
    print 'main'
    #llTests = TestAllTests
    #unittest.TextTestRunner(verbosity=2).run(allTests.suite())
else:
    print "unknown: [{0}]".format(__name__)
    #suite = unittest.TestSuite()
    #suite.addTest(unittest.makeSuite(TestAllTests))

    #allTests = TestAllTests
    #unittest.TextTestRunner(verbosity=2).run(allTests.suite())
    unittest.TextTestRunner(verbosity=2).run(suite())