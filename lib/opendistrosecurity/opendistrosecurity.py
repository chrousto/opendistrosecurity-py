"""
    Base Module for OpenDistro Objects
    DocString has to be completed
"""
from functools import wraps
import logging
import requests
from elasticsearch.client.utils import NamespacedClient
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import AuthenticationException, TransportError

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

    def __init__(self, user, pwd, host='localhost', port=9200, ssl=True):
        self.pwd = pwd
        self.user = user
        self.host = host
        self.pwd = pwd
        self.port = port
        self.ssl = ssl
        self.base_url = f"https://{host}:{port}/"
        self.elastic_search = Elasticsearch(hosts=[f"{self.host}:{self.port}"],
                                use_ssl=self.ssl,
                                http_auth=(self.user, self.pwd)
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
            return True if self.__allowed_keys == _object_keys_list else False
