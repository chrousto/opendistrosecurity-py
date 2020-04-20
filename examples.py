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
tenants_client.create_tenant(tenant="test_tenant",body='{"description":"description test"}')


tenants_dict = tenants_client.get_tenants()
pprint(tenants_dict)

