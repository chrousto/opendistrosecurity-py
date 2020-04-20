import inspect
from functools import wraps
import json
import requests
import logging
import json
from elasticsearch.client.utils import _make_path, NamespacedClient
from elasticsearch import Elasticsearch

# Utils
"""
logger
"""
logger = logging.getLogger(__name__)


def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        logger.debug(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging


class OpenDistro():

    opendistro_path = "_opendistro/_security/api/"

    def __init__(self, user, pwd, host='localhost', port=9200, ssl=True):
        self.user = user
        self.pwd = pwd
        self.host = host
        self.pwd = pwd
        self.port = port
        self.ssl = ssl
        self.base_url = f"https://{host}:{port}/"
        self.es = Elasticsearch(hosts=[f"{self.host}:{self.port}"],
        use_ssl = self.ssl,
        http_auth = ( self.user , self.pwd )
        )
        
               
    def check_connection(self):
        try:
            return True if self.info() else False
        except:
           logger.error("Check Connection : ElasticSearch not reachable")

    def info(self):
        try:
            return self.es.info()
        except:
            raise 

class OpenDistroSecurityObjectClient(NamespacedClient):
    """ 
    Inherits from the ElasticSEarch Py NAmedspacedClient class
    """

    def __init__(self, od):
        assert od is not None
        self.od = od


class OpenDistroSecurityObject:
    """
    Generic Security Object class
    """
    def __init__(self, d):
        """
        Get attributes from json string
        """
        self.__dict__ = d


        
