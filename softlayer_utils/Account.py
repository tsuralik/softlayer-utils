import SoftLayer

def get_details(client):
    retVal = None
    if client != None and isinstance(client, SoftLayer.Client):
        try:
            retVal = client['Account'].getObject()
        except SoftLayer.SoftLayerAPIError as e:
            print("Unable to retrieve account information faultCode=%s, faultString=%s"
                  % (e.faultCode, e.faultString))
            # error handling: use default retVal None 
    return retVal
   
def show_account(client):
    account = get_details(client)
    if account != None and isinstance(account, dict):
        #try:
        print "{0:15} {1:15}".format("ID:", str(account['id']))
        print "{0:15} {1:15}".format("Last Name:", account['firstName'])
        print "{0:15} {1:15}".format("First Name:", account['lastName'])
        print "{0:15} {1:15}".format("Company:", account['companyName'])
        print "{0:15} {1:15}".format("Balance:", client['Account'].getBalance()) 
        return None
        # WOULD THIS ACTUALLY GET RUN NOW?
        #        except SoftLayer.SoftLayerAPIError as e:
        #            print("Unable to retrieve account information faultCode=%s, faultString=%s"
        #                  % (e.faultCode, e.faultString))
        #            #exit(1)
        #            raise e
    else:
        raise BaseException("bad client")
