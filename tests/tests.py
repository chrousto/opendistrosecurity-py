#! /usr/bin/env python
"""
Test cases for the OpenDistro API
"""
import os
import sys
import getpass

import pprint as pp

#Disable the no cert warning
import urllib3 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup the path to the API
this_file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(this_file_dir+'/../lib/opendistrosecurity/'))

from elasticsearch import NotFoundError
from opendistrosecurity import OpenDistro
from tenants import TenantsClient
from roles import RolesClient, OpenDistroRole, IndexPermission, TenantPermission
import roles
import rolesmapping 
import unittest
import sys

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
    ODPWD = getpass.getpass("OpenDistro Password : ") 

OPEN_DISTRO =  OPEN_DISTRO = OpenDistro(host=ODHOST,
                                        port=ODPORT ,
                                        user=ODUSER, 
                                        pwd=ODPWD,
                                        verify_certs=False)
#Check the connection
if (OPEN_DISTRO.check_connection()):
    print(f"\n--> We are able to reach {OPEN_DISTRO.host}")

else:
    print(f"Error : impossible to connectot to {ODHOST}:{ODPORT} with user {ODUSER}")

class TestTenants(unittest.TestCase):
 
    def setUp(self):    
        self.tenants_client = TenantsClient(OPEN_DISTRO)
        print(f"\nNow testing : {self._testMethodName}, result : ",end='')

    def test_gettenants(self):
        tenants = self.tenants_client.get_tenants()
        self.assertNotEqual(len(tenants), 0)        
        self.assertIsInstance(tenants, dict) 
    
    def test_create_and_delete_tenant_low(self):
        """
            Here the goal is to create a tenant and ensure we get it back
            exactly as we had sent it
            AfterWards, we delete it and check it's been deleted
     
            This could be improved by sending the object with the API
            and getting it back via curl for instance

            These tests use the 'Low Level' API that uses built-in python objects 
        """
        #Create a tenant
        _test_tenant_name_request = "_test_tenant"
        _test_tenant_description_request = "_test_tenant_description"
        _body = {"description" : _test_tenant_description_request}

        #Send it to opendistro
        self.tenants_client.create_tenant(tenant=_test_tenant_name_request,
                                          body=_body)

        #Get it back and test what we have
        tenant = self.tenants_client.get_tenant(_test_tenant_name_request)
        self.assertEqual(len(tenant),1)
        _test_tenant_name_response = list(tenant)[0]
        _test_tenant_description_response = tenant[_test_tenant_name_response]["description"]
        self.assertEqual( (_test_tenant_name_request,_test_tenant_description_request),
                          (_test_tenant_name_response,_test_tenant_description_response))
        
    
        #Delete it 
        self.tenants_client.delete_tenant(_test_tenant_name_request)
        
        #Get it back and ensure we have nothing
        with self.assertRaises(NotFoundError):
            tenant = self.tenants_client.get_tenant(_test_tenant_name_request)

class TestRoles(unittest.TestCase):

    def setUp(self):
        self.roles_client = RolesClient(OPEN_DISTRO)
        print(f"\nNow testing : {self._testMethodName}, result : ",end='')
        
    
    def test_getroles(self):
        roles = self.roles_client.get_roles()
        self.assertNotEqual(len(roles), 0)        
        self.assertIsInstance(roles, dict) 
    
    def test_create_and_delete_roles_low(self):
        """
            Here the goal is to create a role ind ensure we get it back
            exactly as we had sent it
            AfterWards, we delete it and check it's been deleted
     
            This could be improved by sending the object with the API
            and getting it back via curl for instance

            These tests use the 'Low Level' API that uses built-in python objects 
        """
        #Create a tenant
        _test_role_name_request = "_test_role"
        _body = {
                    "tenant_permissions" : [
                                            {
                                             "tenant_patterns" : ["tenant1", "tenant2"],
                                             "allowed_actions" : ["kibana_read"]
                                            }
                                           ],
                    "index_permissions" : [ 
                                            {
                                             "index_patterns" : ["index1", "index2"],
                                             "dls" : "{\"_id\":\"example\"",
                                             "fls" : ["~field1", "~field2"],
                                             "masked_fields" : ["field3", "field4"],
                                             "allowed_actions" : ["crud", "example1"]
                                            }
                                          ]
                }

        #Send it to opendistro
        self.roles_client.create_role(role=_test_role_name_request,
                                          body=_body)

        #Get it back and test what we have
        _response_role = self.roles_client.get_role(_test_role_name_request)
        _requested_role = { _test_role_name_request : _body }
        _response_role_params = _response_role[_test_role_name_request]       
        _requested_role_params = _requested_role[_test_role_name_request]       
 
        self.assertEqual(_requested_role_params["index_permissions"], 
                         _response_role_params["index_permissions"])
        self.assertEqual(_requested_role_params["tenant_permissions"], 
                         _response_role_params["tenant_permissions"])
        
        #Delete it 
        self.roles_client.delete_role(_test_role_name_request)
        
        #Get it back and ensure we have nothing
        with self.assertRaises(NotFoundError):
            role = self.roles_client.get_role(_test_role_name_request)

    def test_create_and_delete_roles_high(self):
        
        #Create role        
        _test_role_name_request = "_test_role"
        role_request = OpenDistroRole(_test_role_name_request)
        index_permission1 = IndexPermission()
        index_permission1.addindexpattern("index1*")
        index_permission1.adddls('{"term" : {"field1.1":"true"}}')
        index_permission1.addfls("~filter_me")
        index_permission1.addmaskedfield("mask_me")
        index_permission1.addallowedaction("allowed_action1");
        
        index_permission2 = IndexPermission()
        index_permission2.addindexpattern("index2.1*")
        index_permission2.addindexpattern("index2.2*")
        index_permission2.addindexpattern("index2.3*")
        index_permission2.adddls('{"term" : {"field2.1":"true"}}')
        index_permission2.addfls("~filter_me")
        index_permission2.addmaskedfield("mask_me")
        index_permission2.addallowedaction("allowed_action2");

        tenant_permission1 = TenantPermission()
        tenant_permission1.addtenantpattern("tenant1*")
        tenant_permission1.addtenantpattern("tenant2*")
        tenant_permission1.addtenantpattern("tenant3*")
        tenant_permission1.addallowedaction("allowed_action1")

        role_request.addindexpermission(index_permission1)
        role_request.addindexpermission(index_permission2)
        role_request.addtenantpermission(tenant_permission1)
        
        #Save Role to OpenDistro
        role_request.save(self.roles_client)
        
        #Retrieve Role and validate the fromdict method at the same time
        role_response = OpenDistroRole.fromdict(self.roles_client.get_role(role_request.name))
        
        # Verify some things
        self.assertEqual(role_request.name,role_response.name)
        self.assertEqual(role_request.index_permissions[0].index_patterns[0],
                         role_response.index_permissions[0].index_patterns[0])
        self.assertEqual(role_request.index_permissions[1].index_patterns[1],
                         role_response.index_permissions[1].index_patterns[1])

if __name__ == '__main__':
    unittest.main()
