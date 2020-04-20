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

print("Creating tenants")
tenants_client.create_tenant(tenant="test_tenant",body='{"description":"description test"}')

print("Listing tenants :")
tenants_dict = tenants_client.get_tenants()
pprint(tenants_dict)

print("Deleting tenant ")
tenants_client.delete_tenant("test_tenant")

print("Listing tenants :")
tenants_dict = tenants_client.get_tenants()
pprint(tenants_dict)

