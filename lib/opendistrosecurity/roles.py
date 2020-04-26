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
            :arg role: The name of the role to retrieve
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

    def delete_role(self, role, params=None, headers=None):
        """
            Delete a specific role
            :arg role: The name of the role to retrieve
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
    __allowed_keys = ["description",
                     "reserved",
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
                description=None,
                hidden=False,
                static=False,
                reserved=False):
        """
            Build a role in an OOP way
        """
        try:

            tenant_permissions = [] if tenant_permissions is None else tenant_permissions
            index_permissions = [] if index_permissions is None else index_permissions
            
            role_dict = {}
            role_dict[name] = { "description" : description,
                                "index_permissions" : index_permissions,
                                "cluster_permissions" : cluster_permissions,
                                "tenant_permissions" : tenant_permissions,
                                "hidden" : hidden,
                                "static" : static,
                                "reserved" :reserved}

            super().__init__(role_dict,self.__allowed_keys)
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
    def description(self, description):
        self._object_dict[self.name]["description"] = description 

    @property    
    def index_permissions(self):
        return self._object_dict[self.name]["index_permissions"]

    @index_permissions.setter
    def index_permissions(self, index_permissions):
        self._object_dict[self.name]["index_permissions"] = index_permissions

    @property    
    def tenant_permissions(self):
        return self._object_dict[self.name]["tenant_permissions"]

    @tenant_permissions.setter
    def tenant_permissions(self, tenant_permissions):
        self._object_dict[self.name]["tenant_permissions"] = tenant_permissions

    def addindexpermission(self,index_permission):
        #TODO : Validate what we get 
        self.index_permissions.append(index_permission)

    def addtenantpermission(self,index_permission):
        #TODO : Validate what we get 
        self.tenant_permissions.append(index_permission)

    # Functions for creating and deleting
    def save(self,role_client):
        """
            Save current tenant to an OpenDistro Server
        """
        if (not role_client.open_distro.check_connection()):
            raise Error("OpenDistro is not reachable...")
        try:
            
            index_permissions_list = [ permission.forserialization() for 
                                permission in self.index_permissions ] 
           
            tenant_permissions_list = [ permission.forserialization() for
                                permission in self.tenant_permissions ]

        
            role_client.create_role(role=self.name,
                    body={"index_permissions" : index_permissions_list,
                          "tenant_permissions" : tenant_permissions_list} )
        
        except Exception as e:
            print(e)
            raise ValueError("Unable create role")

    def delete(self,role_client):
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

    def update(self,role_client,description):
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

class TenantPermission(object):
    """
        Class abstracting a tenant permission
        TODO
    """
    def __init__(self,
                 tenant_patterns=None,
                 allowed_actions=None):
        self.tenant_patterns = [] if tenant_patterns is None else tenant_patterns
        self.allowed_actions = [] if allowed_actions is None else allowed_actions

    def addtenantpattern(self,pattern):
        """
            adds an index patterns to the list of index patterns
        """
        self.tenant_patterns.append(pattern)

    def removetenantpattern(self,pattern):
        """ 
            removes a pattern from the list of index patterns
        """
        try:
            self.tenant_patterns.remove(pattern)
        except ValueError:
             print(f"Error : unable to remove {pattern} from the index patterns list")
    #TODO : This part could easily be moved up to an abastract class 
    # in commin with the Index permission object
    def addallowedaction(self,allowed_action):
        """
            Add an allowed action to the list of allowed actions
        """
        self.allowed_actions.append(allowed_action)
    
    def removeallowedaction(self,allowed_action):
        """
            Remove an allowied action from the list of allowed actions
        """
        try:
            self.masked_fields.remove(allowed_action)
        except ValueError:
            print(f"Error : unable to remove masked field {self.masked_field}")
    
    def forserialization(self):
        """
            Poor man's json deserializer
            return a big dict with our objects
            so that we can pass this to ElasticSearch's API for
            json serialization
        """
        return {
                "tenant_patterns" : self.tenant_patterns,
                "allowed_actions" : self.allowed_actions
               }

class IndexPermission():
    """
        Class abstracting an index permission
    """
    def __init__(self,
                index_patterns=None,
                dls=None,
                fls=None,
                masked_fields=None,
                allowed_actions=None):
        """
            :arg index_patterns: List of index patterns
            :arg dls: Document Level Security as a json string
            :arg fls: Field Level Security : List of fields to exclude 
                      Or exclude (prefix with "~" to exclude
            :arg masked_fields: List of fields to mask
            :arg allowed_actions: List of al lowed actions
        """

        self.index_patterns = [] if index_patterns is None else index_patterns
        self.dls = dls
        self.fls = [] if fls is None else fls
        self.masked_fields = [] if masked_fields is None else masked_fields
        self.allowed_actions = [] if allowed_actions is None else allowed_actions
    
    #TODO : This part could easily be moved up to an abastract class 
    # in common with the TenantPermission object
    def addindexpattern(self,pattern):
        """
            adds an index patterns to the list of index patterns
        """
        self.index_patterns.append(pattern)

    def removeindexpattern(self,pattern):
        """ 
            removes a pattern from the list of index patterns
        """
        try:
            self.index_patterns.remove(pattern)
        except ValueError:
             print(f"Error : unable to remove {pattern} from the index patterns list")


    def adddls(self,dls_string):
        """
            add a DLS string that is a json ElasticSearch query
            try / except to ensure it is json
        """
        try:
            json.loads(dls_string)
            self.dls = dls_string
        except ValueError:
            print("Error : dls string is not json")
            print(f"        The string was : {dls_string}")

    def addfls(self,field):
        """
            Adds a field to either include or exclude
            This is a simple list of strings
            for the fields name
            prefix it with ~ for exclusion:

            "~wage" : excludes the wage field
            "friendly" : includes the "friendly" field 
        """
        self.fls.append(field)

    def removefls(self,field):
        try:
            self.fls.remove(field)
        except ValueError:
            print(f"Error : unable to remove {fls}")

    def addmaskedfield(self,masked_field):
        """
            Add a masked field to the list of masked fields
        """
        self.masked_fields.append(masked_field)
    
    def removemaskedfield(self,masked_field):
        """
            Remove a masked field from the list of masked fields
        """
        try:
            self.masked_fields.remove(masked_field)
        except ValueError:
            print(f"Error : unable to remove masked field {self.masked_field}")

    def addallowedaction(self,allowed_action):
        """
            Add an allowed action to the list of allowed actions
        """
        self.allowed_actions.append(allowed_action)
    
    def removeallowedaction(self,allowed_action):
        """
            Remove an allowied action from the list of allowed actions
        """
        try:
            self.masked_fields.remove(allowed_action)
        except ValueError:
            print(f"Error : unable to remove masked field {self.masked_field}")

    def forserialization(self):
        """
            Poor man's json deserializer
            return a big dict with our objects
            so that we can pass this to ElasticSearch's API for
            json serialization
        """
        return {
                "index_patterns" : self.index_patterns,
                "dls" : self.dls,
                "fls" : self.fls,
                "masked_fields": self.masked_fields,
                "allowed_actions" : self.allowed_actions
               }
