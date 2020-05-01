"""
    Base Module for OpenDistro Objects
    DocString has to be completed
"""
from functools import wraps
import logging
from elasticsearch.client.utils import NamespacedClient
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import AuthenticationException, TransportError
from elasticsearch.serializer import JSONSerializer
LOGGER = logging.getLogger(__name__)

def logged(func):
    """
        Utility function for logging
    """
    @wraps(func)
    def with_logging(*args, **kwargs):
        #LOGGER.debug(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging

class OpenDistro():
    """
        High Level Object to access OpenDistro Server running on Elasticsearch
        __init__ :
        :arg user: User to use for connection
        :arg pwd: Password for the connection
        :arg host: Host to connect to
        :arg port: port to connect to
        :arg ssl: Wether to use SSL or not
    """
    opendistro_path = "_opendistro/_security/api/"

    def __init__(self, user, pwd, host='localhost', port=9200, ssl=True,verify_certs=True):
        self.pwd = pwd
        self.user = user
        self.host = host
        self.pwd = pwd
        self.port = port
        self.ssl = ssl
        self.verify_certs = verify_certs
        self.base_url = f"https://{host}:{port}/" if ssl else f"http://{host}:{port}"
        self.elastic_search = Elasticsearch(hosts=[f"{self.host}:{self.port}"],
                                use_ssl=self.ssl,
                                http_auth=(self.user, self.pwd),
                                verify_certs=self.verify_certs
                                )

    def check_connection(self):
        """
            Check is the connection to ES is alive
        """
        try:
            return self.info()
        except AuthenticationException:
            print("Authentication Error in "+__name__)
    def info(self):
        """
            Returns ES Server information
        """
        try:
            return self.elastic_search.info()
        except AuthenticationException:
            print("Authentication Exception")
        except TransportError:
            print("Transport Error")

class OpenDistroSecurityObjectClient(NamespacedClient):
    """
        Inherits from the ElasticSEarch Py aAmedspacedClient class
        It has an OpenDistro Object in order to exchange with the ES instance
    """

    def __init__(self, open_distro):
        assert open_distro is not None
        self.open_distro = open_distro
        super().__init__(self)

class OpenDistroSecurityObject(object):
    
    """
        Generic Security Object class
    """
    def __init__(self, d, allowed_keys):
        """
            Get attributes from json string
        """
        self._object_dict = d
        self.__allowed_keys = allowed_keys
        self.__allowed_keys.sort()
        
        if ( not self._validate()):
            raise ValueError(f"Unable to create this Object of type {type(self)} with these values : {d}")

    def _validate(self):
        """
            This function vaidates that we have the correct keys to send
            To OpenDistro for a specific Security Object
            The list of allowed keys is gotten from the subclass
        """

        _object_keys_list = list(self._object_dict[ list(self._object_dict)[0] ])
        _object_keys_list.sort()
        if (len(self._object_dict) != 1):
            return False
        else:
            return self.__allowed_keys == _object_keys_list

    # Class used to serialize our Various OpenDistro objects and sub-objects
    # We'll see if we use that ...
    # It causes trouble with imports : opendistro imports roles that imports opendistro
    #class Encoder(JSONSerializer):
    #    def default(self, obj):
    #        if(isinstance(obj,IndexPermission)):
    #            return {
    #                "index_patterns" : obj.index_patterns,
    #                "dls" : obj.dls,
    #                "fls" : obj.fls,
    #                "masked_fields": obj.masked_fields,
    #                "allowed_actions" : obj.allowed_actions
    #               }

    #        if(isinstance(obj,TenantPermission)):
    #            return {
    #                    "tenant_patterns" : obj.tenant_patterns,
    #                    "allowed_actions" : obj.allowed_actions
    #                   }


class OpenDistroSecurityException(Exception):
    """
        Base Exception Class
    """
