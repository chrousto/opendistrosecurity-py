"""
Test / Example file for OpenDistro Secuity API
"""

from opendistrosecurity import *
from tenants import *
import json
from pprint import pprint

od = OpenDistro(host="elastique-cherche.chazeau.org",port=443 ,user="admin", pwd="admin")

print("We are Connected ..." if od.check_connection() else "Problem with the connecetion")

tenants_client = TenantsClient(od)
TEST_TENANT = "test_tenant"


print("Creating tenants")
tenants_client.create_tenant(tenant=TEST_TENANT,body='{"description":"description test"}')

print("Listing tenants :")
tenants_dict = tenants_client.get_tenants()
pprint(tenants_dict)

print(f"Getting {TEST_TENANT}")
pprint(tenants_client.get_tenant(TEST_TENANT))

print("Deleting tenant ")
tenants_client.delete_tenant(TEST_TENANT)

print("Listing tenants :")
tenants_dict = tenants_client.get_tenants()
pprint(tenants_dict)

