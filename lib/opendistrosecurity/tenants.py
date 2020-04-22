"""
    This module allows to manipulate tenants !
"""
import json
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

        return self.open_distro.elastic_search.transport.perform_request(
            _method,
            _make_path(
                *OpenDistro.opendistro_path.split("/"),
                self._endpoint),
            params=params,
            headers=headers)

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

        return self.open_distro.elastic_search.transport.perform_request(
            _method,
            _make_path(
                *OpenDistro.opendistro_path.split("/"),
                self._endpoint,
                tenant),
            params=params,
            headers=headers,
            body=body)

class OpenDistroTenant(OpenDistroSecurityObject):
    """
        OpenDistroTenant
    """

    # TODO : improve the json validation with somehting like jsonschema lib
    __allowed_keys = ["reserved","hidden","description","static"]

    def __init__(self, d):
        try:
            super().__init__(d,self.__allowed_keys)

        except:
            raise Exception("Problem when creating tenant object")
    
    @property    
    def name(self):
        return list(self._object_dict)[0]

    @name.setter
    def name(self, name):
        _old_name = list(self._object_dict)[0]
        self._object_dict[name] = self._object_dict.pop( _old_name )

    @property    
    def description(self):
        return self._object_dict[self.name]

    @description.setter
    def description(self, desc):
        self._object_dict[self.name]["description"] = desc

    @property    
    def hidden(self):
        return self._object_dict[self.name]

    @hidden.setter
    def hidden(self, desc):
        self._object_dict[self.name]["hidden"] = desc
    
    @property    
    def static(self):
        return self._object_dict[self.name]

    @static.setter
    def static(self, desc):
        self._object_dict[self.name]["hidden"] = desc


    def display(self):
        """
            Display with Pretty Printer
        """
        pp.pprint(self._object_dict)
