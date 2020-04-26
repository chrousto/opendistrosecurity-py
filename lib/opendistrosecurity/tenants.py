"""
    This module allows to manipulate tenants !
"""
import json
from elasticsearch import ElasticsearchException
from elasticsearch.client.utils import _make_path
from opendistrosecurity import (OpenDistro,
                                OpenDistroSecurityObject,
                                OpenDistroSecurityObjectClient,
                                logged)
import pprint
pp = pprint.PrettyPrinter(indent=4)

class TenantsClient(OpenDistroSecurityObjectClient):
    """
        Client Class that inherits from the generic client
    """
    _endpoint = "tenants"

    def get_tenants(self, params=None, headers=None):
        """
            This function retrieves tenants.
            The HTTP Method as well as the endpoint is guessed from the function
            name, by convention the function is called <method>_<endpoint>
            :arg params: Extra parametrs to pass the URL
            :arg headers: Extra Headers to pass to the request
        """
        _method = "GET"
        
        try:
            return self.open_distro.elastic_search.transport.perform_request(
                                                                _method,
                                                                _make_path(
                                            *OpenDistro.opendistro_path.split("/"),
                                                                self._endpoint),
                                                                params=params,
                                                                headers=headers)
        except ElasticsearchException:
            raise

    def get_tenant(self, tenant, params=None, headers=None):
        """
            Retrieves a specific tenant
            :arg tenant: The name of the tenant to retrieve
            :arg params: Extra parametrs to pass the URL
            :arg headers: Extra Headers to pass to the request
        """
        _method = "GET"

        return self.open_distro.elastic_search.transport.perform_request(
            _method,
            _make_path(
                *OpenDistro.opendistro_path.split("/"),
                self._endpoint,
                tenant),
            params=params,
            headers=headers)

    def delete_tenant(self, tenant, params=None, headers=None):
        """
            Delete a specific tenant
            :arg tenant: The name of the tenant to retrieve
            :arg params: Extra parametrs to pass the URL
            :arg headers: Extra Headers to pass to the request
        """

        _method = "DELETE"

        return self.open_distro.elastic_search.transport.perform_request(
            _method,
            _make_path(
                *OpenDistro.opendistro_path.split("/"),
                self._endpoint,
                tenant),
            params=params,
            headers=headers)

    def create_tenant(self, tenant, body="None", params=None, headers=None):
        """
            Create a specific tenant
            :arg tenant: The name of the tenant to create
            :arg params: Extra parametrs to pass the URL
            :arg headers: Extra Headers to pass to the request
        """
        _method = "PUT"
        try:
            return self.open_distro.elastic_search.transport.perform_request(
                                                            _method,
                                                            _make_path(
                                        *OpenDistro.opendistro_path.split("/"),
                                                            self._endpoint,
                                                            tenant),
                                                            params=params,
                                                            headers=headers,
                                                            body=body)
        except ElasticsearchException:
            raise

class OpenDistroTenant(OpenDistroSecurityObject):
    """
        OpenDistroTenant
        Object to be manipulated
    """

    # TODO : improve the json validation with somehting like jsonschema lib
    __allowed_keys = ["reserved","hidden","description","static"]

    def __init__(self,name,description,hidden=False,static=False,reserved=False):
        """
            Build a tenant in an OOP way
        """
        try:
            tenant_dict = {}
            tenant_dict[name] = {"description" : description,
                                 "hidden" : hidden,
                                 "static" : static,
                                "reserved" : reserved}

            super().__init__(tenant_dict,self.__allowed_keys)
        except:
            raise ValueError("Problem when creating tenant object")

    @classmethod
    def fromdict(cls,tenant_dict):
        # Here we are cheating because we know the json is of the following form:
        # { 'tenant_name': {'description' : "desc", ... } }
        # And we need name=...,desc=... for the init function
        tenant_name = next(iter(tenant_dict))
        tenant_properties = tenant_dict[tenant_name]

        return cls(name = tenant_name , **tenant_properties )

    @property    
    def name(self):
        return list(self._object_dict)[0]

    @name.setter
    def name(self, name):
        _old_name = list(self._object_dict)[0]
        self._object_dict[name] = self._object_dict.pop(_old_name)

    @property    
    def description(self):
        return self._object_dict[self.name]["description"]

    @description.setter
    def description(self, desc):
        self._object_dict[self.name]["description"] = desc

    @property    
    def hidden(self):
        return self._object_dict[self.name]["hidden"]
    
    @property    
    def static(self):
        return self._object_dict[self.name]["static"]

    @property    
    def reserved(self):
        return self._object_dict[self.name]["reserved"]
    

    # Functions for Creating and deleting
    def save(self,tenant_client):
        """
            Save current tenant to an OpenDistro Server
        """
        if (not tenant_client.open_distro.check_connection()):
            raise Error("Not connected to OpenDistro ...")
        try:
            tenant_client.create_tenant(tenant=self.name,
                                        body={"description" : f"{self.description}"})
        except Exception as e:
            raise Error("Unable create tenant")
            print(e)

    def delete(self,tenant_client):
        """
            Delete current tenant from an OpenDistro Server
        """
        if (not tenant_client.open_distro.check_connection()):
            raise Error("Not connected to OpenDistro ...")
        try:
            tenant_client.delete_tenant(tenant=self.name)
        except Exception as e:
            raise Error("Unable delete tenant")
            print(e)

    def upadte(self,tenant_client,description):
        """
            TODO
        """
        pass

    def display(self):
        """
            Pretty pring a tenant
        """
        pp.pprint(self._object_dict)
