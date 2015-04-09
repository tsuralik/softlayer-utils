import argparse
import Client
import json
import SoftLayer.managers
import SoftLayer.exceptions
import sys

def get_vsManager(client): 
    return SoftLayer.managers.vs.VSManager(client)

def find_ID_by_publicIP(client, ip):
    vms = find_vm_by_publicIP(client, ip)
    return vms[0]["id"]

def find_ID_by_hostname(client, hostname):
    vms = find_vm_by_hostname(client, hostname)
    return vms[0]["id"]

def find_publicIP_by_hostname(client, hostname):
    vms = find_vm_by_hostname(client, hostname)
    return vms[0]["primaryIpAddress"]

def find_vm_by_publicIP(client, publicIP):
    vsManager = get_vsManager(client)
    object_mask = "mask[id,hostname,domain,fullyQualifiedDomainName,datacenter,powerState,status,primaryIpAddress]"
    vms = vsManager.list_instances(public_ip=publicIP, mask=object_mask)
    return vms

def find_vm_by_hostname(client, hostname):
    vsManager = get_vsManager(client)
    object_mask = "mask[id,hostname,domain,fullyQualifiedDomainName,datacenter,powerState,status,primaryIpAddress]"
    vms = vsManager.list_instances(hostname=hostname, mask=object_mask)
#   formatter.print_json_listings_w_header(vms, "listing vms with hostname={0}".format(hostname), "vm")
    return vms

def power_on_hostname(client, hostname):
    vmId = find_ID_by_hostname(client, hostname)
    power_on_id(client, vmId, hostname)

def power_on_ip(client, ip):
    vmId = find_ID_by_publicIP(client, ip)
    power_on_id(client, vmId, ip)

def power_on_id(client, vmId, descriptor = "?"):
    vGuestObject = client['Virtual_Guest'] 
    try:  
        print "powering on {0} ({1}): {2}".format(vmId, descriptor, vGuestObject.powerOn(id=vmId))
    except SoftLayer.exceptions.SoftLayerAPIError as error:
        print "powering on {0} ({1}): FAILED : {1} | {2}".format(vmId, descriptor, error.faultCode, error.faultString)

def power_on_all(client):
    vGuestObject = client['Virtual_Guest'] 
    vms = get_vms(client)
    for vm in vms:
        print "powering on {0}: {1}".format(vm["hostname"],vGuestObject.powerOn(id=vm["id"]))

def power_off_hostname(client, hostname):
    vmId = find_ID_by_hostname(client, hostname)
    power_off_id(client, vmId, hostname)
    
def power_off_ip(client, ip):
    vmId = find_ID_by_publicIP(client, ip)
    power_off_id(client, vmId, ip)

def power_off_id(client, vmId, descriptor = "?"):
    vGuestObject = client['Virtual_Guest'] 
    try:  
        print "powering off {0} ({1}): {2}".format(vmId, descriptor, vGuestObject.powerOff(id=vmId))
    except SoftLayer.exceptions.SoftLayerAPIError as error:
        print "powering off {0} ({1}): FAILED : {2} | {3}".format(vmId, descriptor, error.faultCode, error.faultString)

def power_off_all(client):
    vGuestObject = client['Virtual_Guest'] 
    vms = get_vms(client)
    for vm in vms:
        power_off_id(client, vm["id"])

def list_hardware(client): 
    print 'listing hardware:'
    print '----------------'
    hardware_manager = SoftLayer.HardwareManager(client)
    hardware = hardware_manager.list_hardware()
    print hardware 
    print '----------------'

def get_vms(client, object_mask=None): 
    vsManager = get_vsManager(client)
    if object_mask == None:
        vms = vsManager.list_instances() 
    else:
        vms = vsManager.list_instances(mask=object_mask) 
    return vms

def list_vms_power(client): 
    object_mask = "mask[id,hostname,domain,fullyQualifiedDomainName,datacenter,powerState,status,primaryIpAddress]"
    vms = get_vms(client, object_mask)
    print json.dumps(vms, indent=4)

def list_vms(client): 
    vms = get_vms(client)
    print json.dumps(vms, indent=4)

def create_vm(): 
    print 'create a vm'

def destroy_vm():
    print 'destroy the vm'

def process(process_args):
    print 'process: {0}'.format(process_args)
    if process_args.list:
        print "do list"
        client = Client.get_client(process_args.client)
        list_vms(client)
    else:
        print "do something else"
    
# Parse the command line arguments via argparse.ArgumentParser.
# 
# Run with --help to view description of valid arguments.
#
# arg: args - list of the command line arguments
# Return value: the args dict returned from parser.parse_args(args)
def parseArgs(args):
    parser = argparse.ArgumentParser(description='SoftLayer Management VM Tool')
    parser.add_argument("client", help="The name of the client hosting the machine(s)")
    parser.add_argument("--list", help="Flag to list all machines", action="store_true")
    return parser.parse_args(args)
   
if __name__ == '__main__':
    commandLine_args = sys.argv[1:] # get the command line arguments excluding the class name
    process_args = parseArgs(commandLine_args)
    process(process_args)
