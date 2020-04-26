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
from roles import *
from rolesmapping import *
import json
from pprint import pprint

## Get Env vars
ODHOST = os.environ.get('ODHOST')
ODPORT= os.environ.get('ODPORT')
ODUSER = os.environ.get('ODUSER')
ODPWD = os.environ.get('ODPWD')

# If nothing, ask
if(ODHOST is None):
    print("OpenDistro Address : ")
    ODHOST = input()

if(ODPORT is None):
    print("OpenDistro Port : ")
    ODPORT = input()

if(ODUSER is None):
    print("OpenDistro User : ")
    ODUSER = input()

if(ODPWD is None):
    print("OpenDistro Password : ")
    ODPWD = input()

#Create OpenDistro Connection
od = OpenDistro(host=ODHOST,
                port=ODPORT,
                user=ODUSER, 
                pwd=ODPWD)

#Check the connection
if (od.check_connection()):
    print(">>> We are Connected ...")
else: 
    print(f"Problem with connecting to {od.host}:{od.port} with user {od.user}")
    exit(1)

# TENANTS
#Create a Tenant Client for direct lowlevel objects creations
tenants_client = TenantsClient(od)
test_tenant_name_lowlevel = "_test_tenant_lowlevel"
test_tenant_name_highlevel = "_test_tenant_highlevel"
test_tenant_name_highlevel_updated = "_updated_test_tenant_highlevel"

print(">>> TENANTS >>>")
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
created_tenant_sets = (test_tenant_name_lowlevel,
                       test_tenant_name_highlevel,
                       test_tenant_name_highlevel_updated) 
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

# ROLES
#Create a Role Client for direct lowlevel objects creations
roles_client = RolesClient(od)
test_role_name_lowlevel = "_test_role_lowlevel"
test_role_name_highlevel = "_test_role_highlevel"
test_role_name_highlevel_updated = "_updated_test_role_highlevel"

index_permission1 = IndexPermission()
index_permission1.addindexpattern("index1.1*")
index_permission1.addindexpattern("index1.2*")
index_permission1.addindexpattern("index1.3*")
index_permission1.adddls('{"term" : {"field1.1":"true"}}')
index_permission1.addfls("~filter_me")
index_permission1.addmaskedfield("mask_me")
index_permission1.removeindexpattern("index1.3*")
index_permission1.addallowedaction("allowed_action1");

index_permission2 = IndexPermission()
index_permission2.addindexpattern("index2.1*")
index_permission2.addindexpattern("index2.2*")
index_permission2.addindexpattern("index2.3*")
index_permission2.adddls('{"term" : {"field2.1":"true"}}')
index_permission2.addfls("~filter_me")
index_permission2.addmaskedfield("mask_me")
index_permission2.removeindexpattern("index2.3*")
index_permission2.addallowedaction("allowed_action2");

tenant_permission1 = TenantPermission()
tenant_permission1.addtenantpattern("tenant1*")
tenant_permission1.addtenantpattern("tenant2*")
tenant_permission1.addtenantpattern("tenant3*")
tenant_permission1.addallowedaction("allowed_action1")



r = OpenDistroRole(name=test_role_name_highlevel,
                   index_permissions=[index_permission1 , index_permission2],
                   tenant_permissions=[tenant_permission1]
                   )

print(r._object_dict)

print(">>> ROLES  >>>")
print(">>> Creating a role with the low level methods")
roles_client.create_role(role=test_role_name_lowlevel,body='{"description":"This role was created for testing purpose with the lowlevel API"}')
print(">>> Creating a role with the high level methods")
r.save(roles_client)
r.delete(roles_client)

rolesmapping_client = RolesMappingClient(od)
rm = rolesmapping_client.get_rolesmappings()
rm = OpenDistroRoleMapping(role_name="tests")
print(rm.__dict__)
rm.adduser("plop")
rm.addbackendrole("ohyeah")
rm.addhost("host")
rm.save(rolesmapping_client)
