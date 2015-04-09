import Client
import unittest

class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestClient, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestClient, cls).tearDownClass()

    #def setUp(self):

    #def tearDown(self):
        
    def test_get_unspecified_client(self):
        retVal = Client.get_client()
        self.assertEquals(retVal, None)
        
    def test_get_unknown_client(self):
        retVal = Client.get_client('Bill Murray - aka Venkman')
        self.assertEquals(retVal, None)
        
    def test_get_client_with_bad_data(self):
        retVal = Client.get_client(['array'])
        self.assertEquals(retVal, None)
        
    def test_get_client_for_tsuralik_returns_a_client(self):
        retVal = Client.get_client('tsuralik')
        self.assertNotEquals(retVal, None)
        
    def test_get_client_for_tsuralik_returns_with_proper_key(self):
        retVal = Client.get_client('tsuralik')
        self.assertNotEquals(retVal, None)
        #Client: <Client: endpoint=https://api.softlayer.com/xmlrpc/v3.1, user=<BasicAuthentication: tsuralik>>
   
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestClient))
    return suite

if __name__ == '__main__':
    unittest.main()