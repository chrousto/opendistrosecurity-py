"""
    This module allows to manipulate Roles !
"""
import json
from elasticsearch.client.utils import _make_path
from opendistrosecurity import (OpenDistro,
                                OpenDistroSecurityObject,
                                OpenDistroSecurityObjectClient,
                                logged)
import pprint
pp = pprint.PrettyPrinter(indent=4)

class RolesClient(OpenDistroSecurityObjectClient):
    """
        Client Class that inherits from the generic client
    """
    _endpoint = "roles"

    def get_roles(self, params=None, headers=None):
        """
            This function retrieves roles.
            The HTTP Method as well as the endpoint is guessed from the function
            name, by convention the function is called <method>_<endpoint>
            :arg params: Extra parametrs to pass the URL
            :arg headers: Extra Headers to pass to the request
        """
        _method = "GET"

        return self.open_distro.elastic_search.transport.perform_request(
            _method,
            _make_path(
                *OpenDistro.opendistro_path.split("/"),
                self._endpoint),
            params=params,
            headers=headers)

    def get_role(self, role, params=None, headers=None):
        """
            Retrieves a specific role
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
                role),
            params=params,
            headers=headers)

    def delete_tenant(self, role, params=None, headers=None):
        """
            Delete a specific role
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
                role),
            params=params,
            headers=headers)

    def create_role(self, role, body="None", params=None, headers=None):
        """
            Create a specific role
            :arg tenant: The name of the tenant to create
            :arg params: Extra parametrs to pass the URL
            :arg headers: Extra Headers to pass to the request
        """
        _method = "PUT"

        return self.open_distro.elastic_search.transport.perform_request(
            _method,
            _make_path(
                *OpenDistro.opendistro_path.split("/"),
                self._endpoint,
                role),
            params=params,
            headers=headers,
            body=body)

class OpenDistroRole(OpenDistroSecurityObject):
    """
        OpenDistroRole
        Object to be manipulated
    """

    # TODO : improve the json validation with somehting like jsonschema lib
    __allowed_keys = ["reserved",
                     "hidden",
                     "static",
                     "index_permissions",
                     "cluster_permissions",
                     "tenant_permissions"]

    def __init__(self,
                name,
                index_permissions=None,
                cluster_permissions=None,
                tenant_permissions=None,
                hidden=False,
                static=False,
                reserved=False):
        """
            Build a tenant in an OOP way
        """
        try:
            role_dict = {}

            super().__init__(tenant_dict,self.__allowed_keys)
        except:
            raise ValueError("Problem when creating tenant object")

    @classmethod
    def fromdict(cls,tenant_dict):
        # Here we cheat because we know the json is of the following form:
        # { 'tenant_name': {'description' : "desc", ... } }
        # And we need name=...,desc=... for the init function
        role_name = next(iter(tenant_dict))
        rolet_properties = tenant_dict[tenant_name]

        return cls(name = role_name , **role_properties )

    @property    
    def name(self):
        return list(self._object_dict)[0]

    @name.setter
    def name(self, name):
        _old_name = list(self._object_dict)[0]
        self._object_dict[name] = self._object_dict.pop(_old_name)

    # Functions for Creating and deleting
    def save(self,role_client):
        """
            Save current tenant to an OpenDistro Server
        """
        if (not role_client.open_distro.check_connection()):
            raise Error("Not connected to OpenDistro ...")
        try:
            role_client.create_role(tenant=self.name,
                                        body={"description" : f"{self.description}"})
        except Exception as e:
            raise Error("Unable create role")
            print(e)

    def delete(self,rolet_client):
        """
            Delete current tenant from an OpenDistro Server
        """
        if (not role_client.open_distro.check_connection()):
            raise Error("Not connected to OpenDistro ...")
        try:
            role_client.delete_role(role=self.name)
        except Exception as e:
            raise Error("Unable delete tenant")
            print(e)

    def upadte(self,role_client,description):
        """
            TODO
        """
        pass

    def display(self):
        """
            Pretty pring a tenant
        """
        pp.pprint(self._object_dict)
