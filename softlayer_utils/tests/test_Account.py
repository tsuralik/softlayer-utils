import Account
import Client
import SoftLayer
import unittest

class TestAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccount, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestAccount, cls).tearDownClass()

    def setUp(self):
        self.client = Client.get_client('tsuralik')
        self.account = Account

    def tearDown(self):
        self.client = None
        
    def test_client_setup(self):
        self.assertNotEquals(self.client, None)
        
    def test_get_account_with_no_client(self):
        retVal = Account.get_details(None)
        self.assertEquals(retVal, None)
        
    def test_get_account_with_invalid_client(self):
        retVal = Account.get_details('string')
        self.assertEquals(retVal, None)
        
    def test_get_account_with_client(self):
        details = Account.get_details(self.client)
        expectedDict = {'lastName': 'john doe', 
                        'city': 'Reston',
                        'postalCode': '20194', 
                        'modifyDate': '', 
                        'lateFeeProtectionFlag': '', 
                        'firstName': 'john doe', 
                        'companyName': 'company name', 
                        'address1': '1 Main Street', 
                        'accountManagedResourcesFlag': False, 
                        'accountStatusId': 1001, 
                        'statusDate': '', 
                        'brandId': 2, 
                        'email': 'john.doe@gmail.com', 
                        'state': 'VA', 
                        'allowedPptpVpnQuantity': 1, 
                        'country': 'US', 
                        'id': 000001, 
                        'officePhone': '7035550001', 
                        'isReseller': 0, 
                        'createDate': '2014-10-02T18:39:47-06:00', 
                        'claimedTaxExemptTxFlag': False}

        self.assertDictEqual(details, expectedDict)
        
    def test_bad_account_(self):
        bad_client = Client.get_client('mustafa') # from the lion-king
        details = Account.get_details(bad_client)
        self.assertEquals(details, None)
        
    def test_show_account_with_a_valid_account(self): 
        client = Client.get_client('tsuralik') 
        retVal = Account.show_account(client)
        self.assertEquals(retVal, None)
        
    def test_show_account_with_a_invalid_account(self): 
        client = Client.get_client('mustafa') # from the lion-king
        try:
            Account.show_account(client)
        except SoftLayer.SoftLayerAPIError as slAPIe:
            pass
        except BaseException as be:
            self.assertEquals(be.message, "bad client")
        else:
            self.fail("expected a SoftLayer.SoftLayerAPIError")
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAccount))
    return suite
        
if __name__ == '__main__':
    unittest.main()
