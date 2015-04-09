#import argparse
import Account
import Client
#import MyFormatter
#import SoftLayer
#import VmManager

def go():
    #MyFormatter.print_program_start()

    #parser = argparse.ArgumentParser(description='SoftLayer Management Tool')
    #parser.add_argument("echo", help="Echo Repeated")
    #args = parser.parse_args()
   
    #print args.echo
    
    client = Client.get_client('tsuralik') 
    
    if client != None:   
        account = Account
        acct_details = account.get_details(client)
        account.show_account(client)

    print "Finished!"
#    vmManager = VmManager
#    vmManager.list_vms(client)
#    vmManager.power_off_all(client)
#    vmManager.list_vms(client)

    #MyFormatter.print_program_end()

go()
