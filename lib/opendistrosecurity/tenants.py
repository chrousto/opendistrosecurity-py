"""
    This module allows to manipulate tenants !
"""
from elasticsearch.client.utils import _make_path
from opendistrosecurity import (OpenDistro,
                                OpenDistroSecurityObject,
                                OpenDistroSecurityObjectClient,
                                logged)

class TenantsClient(OpenDistroSecurityObjectClient):
    """
        Client Class that inherits from the generic client
    """
    _endpoint = "tenants"

    @logged
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

    @logged
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

    @logged
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

    @logged
    def create_tenant(self, tenant, body="None", params=None, headers=None):
        """
            Delete a specific tenant
            :arg tenant: The name of the tenant to retrieve
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
        OpenDistroTenant Abstract Object
    """

    def __init__(self,  ):
        self._dict_ = d
        super().__init__()

    def display(self):
        """
            Display
        """
        print("Let's display "+self)

    def hidden(self):
        """
            is hidden ?
        """
        print("Am I hidden ? "+self)
