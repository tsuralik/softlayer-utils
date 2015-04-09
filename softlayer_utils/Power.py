import argparse
import Client
import sys
import VmManager

class Power:

    # Get a SoftLayer Client instance for the specified user.
    #
    # arg: name - the name of the user for the Client instance
    # Return value: the SoftLayer Client instance
    def getClient(self, name):
        return Client.get_client(name)

    # Get a VmManager instance
    #
    # Return value: a VmManager instance
    def getVmManager(self):
        return VmManager
    
    # Toggle power on one or all machines attributable to a specified user
    #
    # Run with --help to view description of valid arguments.
    #
    # arg: args - list of the command line arguments
    def togglePower(self, args):
    
        client = self.getClient(args.client) 
        if client != None:
            vmManager = self.getVmManager()
            if vmManager != None:            
                if args.power == 'on':
                    if args.all:
                        vmManager.power_on_all(client)
                    elif args.id:
                        vmManager.power_on_id(client, args.id)
                    elif args.ip:
                        vmManager.power_on_ip(client, args.ip)
                    elif args.hostname:
                        vmManager.power_on_hostname(client, args.hostname)
                    else:
                        print "power machines on"
                elif args.power == "off":
                    if args.all:
                        vmManager.power_off_all(client)
                    elif args.id:
                        vmManager.power_off_id(client, args.id)
                    elif args.ip:
                        vmManager.power_off_ip(client, args.ip)
                    elif args.hostname:
                        vmManager.power_off_hostname(client, args.hostname)
                    else:
                        print "power machines off"
                elif args.power == "list":
                    vmManager.list_vms_power(client)
            
                if args.list:
                    vmManager.list_vms_power(client)
        else:
            print "A client must be named and exist in the system"    
            
    # Parse the command line arguments via argparse.ArgumentParser.
    # 
    # Run with --help to view description of valid arguments.
    #
    # arg: args - list of the command line arguments
    # Return value: the args dict returned from parser.parse_args(args)
    def parseArgs(self, args):
        parser = argparse.ArgumentParser(description='SoftLayer Management Power Tool')
        parser.add_argument("client", help="The name of the client hosting the machine(s)")
        parser.add_argument("power", choices=["on", "off", "list"], help="Whether power should be turned on or off or listed")
        power_options = parser.add_mutually_exclusive_group(required=True)
        power_options.add_argument("--all", help="Flag to cycle all machines", action="store_true")
        power_options.add_argument("--id", help="The id of the machine to cycle")
        power_options.add_argument("--ip", help="The IP of the machine to cycle")
        power_options.add_argument("--hostname", help="The hostname of the machine to cycle")
        parser.add_argument("--list", help="list VM status after power cycle is complete", action="store_true")
        return parser.parse_args(args)
   
if __name__ == '__main__':
    commandLine_args = sys.argv[1:] # get the command line arguments excluding the class name
    power_util = Power()
    process_args = power_util.parseArgs(commandLine_args)
    power_util.togglePower(process_args)
