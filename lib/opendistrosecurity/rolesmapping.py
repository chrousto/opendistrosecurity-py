"""
    This module allows RolesMapping manipulation
"""
import json
from elasticsearch.client.utils import _make_path
from opendistrosecurity import (OpenDistroSecurityObject,
                                OpenDistroSecurityObjectClient,
                                logged)
import pprint
pp = pprint.PrettyPrinter(indent=4)

class RolesMappingClient(OpenDistroSecurityObjectClient):
    """
        Client Class that inherits from the generic client
    """

    def get_rolesmappings(self, params=None, headers=None):
        """
            This function retrieves rolesmappings.
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

    def get_rolemapping(self, role, params=None, headers=None):
        """
            Retrieves a specific role
            :arg role: The name of the role to retrieve the mapping of
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

    def delete_rolemapping(self, role, params=None, headers=None):
        """
            Delete the mappings for a role
            :arg role: The name of the role to delete the mapping of 
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

    def create_rolemapping(self, role, body="None", params=None, headers=None):
        """
            Create a specific role mapping
            :arg role: The name of the role to create
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

class OpenDistroRoleMapping(OpenDistroSecurityObject):
    """
        OpenDistroRole
        Object to be manipulated
    """
    # TODO : improve the json validation with somehting like jsonschema lib
    __allowed_keys = ["reserved",
                     "static",
                     "hidden",
                     "backend_roles",
                     "hosts",
                     "users"]

    def __init__(self,
                role_name,
                backend_roles=None,
                hosts=None,
                users=None,
                hidden=False,
                static=False,
                reserved=False):
        """
            Build a role in an OOP way
        """
        try:
            role_mapping = {}
            self._name = role_name
            _backend_roles = [] if backend_roles is None else backend_roles
            _hosts = [] if hosts is None else hosts
            _users = [] if users is None else users

            role_mapping[role_name] = { "backend_roles" : _backend_roles,
                                        "hosts" : _hosts,
                                        "users" : _users,
                                        "hidden" : hidden,
                                        "static" : static,
                                        "reserved" : reserved}
             
            super().__init__(role_mapping,self.__allowed_keys)
        except:
            raise ValueError("Problem when creating role object")

    @classmethod
    def fromdict(cls,role_dict):
        # Here we are cheating because we know the json is of the following form:
        # { 'role_name': {'index_permissions' : [ ... , ... ] , ... } }
        role_name = next(iter(role_dict))
        role_properties = role_dict[role_name]
        return cls(name = role_name , **role_properties )

    @property    
    def role_name(self):
        return list(self._object_dict)[0]

    @role_name.setter
    def role_name(self, name):
        _old_name = list(self._object_dict)[0]
        self._object_dict[name] = self._object_dict.pop(_old_name)

    @property    
    def backend_roles(self):
        return self._object_dict[self._name]["backend_roles"]

    @backend_roles.setter
    def backend_roles(self, roles):
        self._object_dict[self._name]["backend_roles"] = roles

    @property    
    def users(self):
        return self._object_dict[self._name]["users"]

    @users.setter
    def users(self, users):
        self._object_dict[self._name]["users"] = users 
    
    @property    
    def hosts(self):
        return self._object_dict[self._name]["hosts"]

    @hosts.setter
    def hosts(self, users):
        self._object_dict[self.name]["hosts"] = hosts 

    # Functions for manipulating Roles mapping
    def adduser(self,user):
        self.users.append(user)

    def addhost(self,host):
        self.hosts.append(host)

    def addbackendrole(self,backendrole):
        self.backend_roles.append(backendrole)

    # Functions for creating and deleting
    def save(self,rolesmapping_client):
        """
            Save current tenant to an OpenDistro Server
        """
        if (not rolesmapping_client.open_distro.check_connection()):
            raise Error("Not connected to OpenDistro ...")
        try:
       
            rolesmapping_client.create_rolemapping(role=self.role_name,
                    body={"backend_roles" : self.backend_roles,
                          "users" : self.users,
                          "hosts" : self.hosts} )
        
        except Exception as e:
            raise ValueError("Unable create role")
            print(e)

    def delete(self,rolesmapping_client):
        """ 
            Delete current tenant from an OpenDistro Server
        """
        if (not rolesmapping_client.open_distro.check_connection()):
            raise Error("Not connected to OpenDistro ...")
        try:
            rolesmapping_client.delete_roleimapping(role=self.role_name)
        except Exception as e:
            raise Error("Unable delete tenant")
            print(e)

    def update(self,rolesmapping_client,description):
        """
            TODO
        """
        pass

    def display(self):
        """
            Pretty pring a role
        """
        pp.pprint(self._object_dict)
    
    def __repr__(self):
        self.display();
