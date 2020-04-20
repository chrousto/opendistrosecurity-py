from opendistrosecurity import *
from elasticsearch.client.utils import _make_path

class TenantsClient(OpenDistroSecurityObjectClient):

    _endpoint = "tenants"

    @logged
    def get_tenants(self, params=None, headers=None):
        """
        This function retrieves tenants.
        The HTTP Method as well as the endpoint is guessed from the function
        name, by convention the function is called <method>_<endpoint>
        """
        _method = "GET"
        
        return self.od.es.transport.perform_request(
            _method ,
            _make_path(*OpenDistro.opendistro_path.split("/"), 
            self._endpoint), 
            params=params, 
            headers=headers)

    @logged
    def get_tenant(self, tenant, params=None, headers=None):
        """
        Retrieves a specific tenant
        """
        _method = "GET"

        return self.od.es.transport.perform_request(
            _method ,
            _make_path(*OpenDistro.opendistro_path.split("/"),
            self._endpoint, tenant),
            params=params,
            headers=headers)
   
    @logged
    def delete_tenant(self, tenant, params=None, headers=None):
        """
        Delete a specific tenant
        """
        _method = "DELETE"

        return self.od.es.transport.perform_request(
            _method ,
            _make_path(*OpenDistro.opendistro_path.split("/"),
            self._endpoint, tenant),
            params=params,
            headers=headers)

    @logged
    def create_tenant(self, tenant, body="None", params=None, headers=None):
        """
        Delete a specific tenant
        """
        _method = "PUT"

        return self.od.es.transport.perform_request(
            _method ,
            _make_path(*OpenDistro.opendistro_path.split("/"),
            self._endpoint, tenant),
            params=params,
            headers=headers,
            body=body)



class OpenDistroTenant(OpenDistroSecurityObject):
    def __init__():
        return True

