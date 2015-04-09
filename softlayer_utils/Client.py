import argparse
import json
import SoftLayer
import sys

# TODO: update keys for bruce and phil
__TEAM = {
        'tsuralik'      :   'add-here',
        'bgoldfeder'    :   'add-here',
        'pstivason'     :   'add-here'
    }

def get_client(name=None): 
    # INITIAL TESTING PARAMETERS
    # endpoint_url="https://api.softlayer.com/xmlrpc/v3.1",
    # endpoint_url=SoftLayer.API_PRIVATE_ENDPOINT,
    retVal = None
    if name != None and isinstance(name, str) and (name in __TEAM):
        key = __TEAM[name]        
        retVal = SoftLayer.Client(username=name, api_key=key, timeout=30)

    return retVal

def list_account(client):
    print "account is: {0}:".format(client)

def list_ssh_keys(client):
    print "{0:15} {1:15}".format("SSH Keys:", json.dumps(client['Account'].getSshKeys(), indent=4))

def process_command_line_args(args):
    client = get_client(args.client)
    
    if args.sshkeys:
        list_ssh_keys(client)
    else:
        list_account(client)
        
# Parse the command line arguments via argparse.ArgumentParser.
# 
# Run with --help to view description of valid arguments.
#
# arg: args - list of the command line arguments
# Return value: the args dict returned from parser.parse_args(args)
def parse_command_line(args):
    parser = argparse.ArgumentParser(description='Altas FCC Context Switching Tool')
    parser.add_argument("client", help="the name of the client")
    parser.add_argument("--sshkeys", action="store_true", help="list the sshkeys for the client")
    return parser.parse_args(args)

if __name__ == '__main__':
    process_args = sys.argv[1:] # get the command line arguments excluding the class name
    commandLine_args = parse_command_line(process_args)
    process_command_line_args(commandLine_args)
