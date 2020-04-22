"""
Test / Example file for OpenDistro Secuity API
"""
import os
import sys
sys.path.insert(0, os.path.abspath('../lib/opendistrosecurity'))

from opendistrosecurity import *
from tenants import *
import json
from pprint import pprint

od = OpenDistro(host="elastique-cherche.chazeau.org",port=443 ,user="admin", pwd="admin")

print(">>> We are Connected ..." if od.check_connection() else "Problem with the connecetion")

tenants_client = TenantsClient(od)
TEST_TENANT = "test_tenant"

print(">>> Creating tenant from within the body")
tenants_client.create_tenant(tenant=TEST_TENANT,body='{"description":"description test"}')

print(">>> Creating tenant by building a Tenant Object")
tenant_dict = { "Tenant Creatd with an object" : { "description":"Tenant Object description","hidden":False,"static":False,"reserved":False } }
tenant_object = OpenDistroTenant(tenant_dict)
tenant_object.display()
print(">>> Updating this tenant name")
tenant_object.description = "Updated Tenant Description"
tenant_object.name = "Updated Tenant Name"
tenant_object.display()

print(">>> Listing tenants :")
tenants_dict = tenants_client.get_tenants()
pprint(tenants_dict)

print(f">>> Getting {TEST_TENANT}")
tenant_dict = tenants_client.get_tenant(TEST_TENANT)
tenant = OpenDistroTenant(tenant_dict)
tenant.display()


print(">>> Deleting tenant ")
tenants_client.delete_tenant(TEST_TENANT)

print(">>> Listing tenants :")
tenants_dict = tenants_client.get_tenants()
pprint(tenants_dict)
