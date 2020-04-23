"""
Test / Example file for OpenDistro Secuity API
TODO : Implement with unittest
"""
import os
import sys
this_file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(this_file_dir+'/../lib/opendistrosecurity'))

from opendistrosecurity import *
from tenants import *
import json
from pprint import pprint

#Create OpenDistro Connection
od = OpenDistro(host="elastique-cherche.chazeau.org",
                port=443 ,
                user="admin", 
                pwd="admin")

#Check the connection
if (od.check_connection()):
    print(">>> We are Connected ...")
else: 
    print(f"Problem with connecting to {od.host}:{od.port} with user {od.user}")
    exit(1)

#Create a Tenant Client for direct lowlevel objects creations
tenants_client = TenantsClient(od)
test_tenant_name_lowlevel = "_test_tenant_lowlevel"
test_tenant_name_highlevel = "_test_tenant_highwlevel"
test_tenant_name_highlevel_updated = "_updated_test_tenant_highlevel"

print(">>> Creating a tenant with the lowlevel methods")
tenants_client.create_tenant(tenant=test_tenant_name_lowlevel,body='{"description":"This tenant was created for testing purpose with the lowlevel API"}')

print(">>> Creating tenant with Objects (High level API)")
tenant_object = OpenDistroTenant(name=test_tenant_name_highlevel,
                                 description="This tenant was created for testing purposes with the High Level API")
print(">>> Display the created tenant :")
tenant_object.display()
print(">>> Saving the created tenant to OpenDistro")
tenant_object.save(tenants_client)
print(">>> Updating this tenant's name and decription")
tenant_object.description = "This tenant was created for testing purposes with the High Level API - Updated"
tenant_object.name = test_tenant_name_highlevel_updated 
tenant_object.save(tenants_client)
print(">>> Display the updatedtenant :")
tenant_object.display()

print(">>> Listing tenants from the server:")
created_tenant_sets = ( test_tenant_name_lowlevel, test_tenant_name_highlevel, test_tenant_name_highlevel_updated ) 
tenants_dict = tenants_client.get_tenants()
if all (tenant in tenants_dict for tenant in created_tenant_sets):
    print("     >>> Success : All created tenants found")
else:
    print("     >>> Error : Not found our tenants :(")
print(">>> Print every tenant we find : ")
pprint(tenants_dict.keys())

print(">>> Deleting created test tenants (with low level api)")
[ tenants_client.delete_tenant(tenant) for tenant in created_tenant_sets ]

print(">>> Checking that everything has been deleted")
tenants_dict = tenants_client.get_tenants()
if any(tenant in tenants_dict for tenant in created_tenant_sets):
    print("     >>> Error : A test tenant has not been deletedi :(")
else:
    print("     >>> Success : Not found any of ourtenants :)")
print(">>> Print every tenant we find : ")
pprint(tenants_dict.keys())
