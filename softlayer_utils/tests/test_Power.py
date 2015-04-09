import Power
import unittest

class TestPower(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPower, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestPower, cls).tearDownClass()

    #def setUp(self):

    #def tearDown(self):
   
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPower))
    return suite

if __name__ == '__main__':
    unittest.main()