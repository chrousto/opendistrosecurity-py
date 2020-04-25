#! /usr/bin/env python
"""
Test cases for the OpenDistro API
"""
import os
import sys
# Setup the path to the API
this_file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(this_file_dir+'/../lib/opendistrosecurity'))

from elasticsearch import NotFoundError
from opendistrosecurity import OpenDistro
from tenants import TenantsClient
from roles import RolesClient
import roles
import rolesmapping 
import unittest
import sys

HOST = "elastique-cherche.chazeau.org"
PORT = 443
USER = "admin"
PWD = "admin"
OPEN_DISTRO =  OPEN_DISTRO = OpenDistro(host=HOST,
                                             port=PORT ,
                                            user=USER, 
                                            pwd=PWD)

class TestTenants(unittest.TestCase):
 
    def setUp(self):

        #Check the connection
        if (OPEN_DISTRO.check_connection()):
            print(f"\n--> We are (still) able to reach {OPEN_DISTRO.host}")

            self.tenants_client = TenantsClient(OPEN_DISTRO)
        else:
            print(f"Not connected to {OPEN_DISTRO.host}")
            raise Exception(f"Unable to connect to OpenDistro {OPEN_DISTRO.host}") 

        print(f"Now testing : {self._testMethodName}")

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
        #Create OpenDistro Connection
        OPEN_DISTRO = OpenDistro(host=HOST,
                                      port=PORT,
                                      user=USER, 
                                      pwd=PWD)

        #Check the connection
        if (OPEN_DISTRO.check_connection()):
            print(f"--> We are (still) connected to {OPEN_DISTRO.host}")
            self.roles_client = RolesClient(OPEN_DISTRO)
        else:
            print(f"Not connected to {OPEN_DISTRO.host}")
            raise Exception(f"Unable to connect to OpenDistro {OPEN_DISTRO.host}") 
    
    def test_getroles(self):
        roles = self.roles_client.get_roles()
        self.assertNotEqual(len(roles), 0)        
        self.assertIsInstance(roles, dict) 

if __name__ == '__main__':
    unittest.main()
