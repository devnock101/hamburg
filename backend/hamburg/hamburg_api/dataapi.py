"""Business Logic Layer"""

import logging
import requests
from hamburg.settings import MOVIEDB_API_KEY,\
        MOVIEDB_API_SEARCH, MOVIEDB_API_BASE, MOVIEDB_API_REGION,\
        MOVIEDB_API_LANG

LOGGER = logging.getLogger(__name__)

class MovieDBResults():
    """Class for all data related to MovieDB"""
    def __init__(self):
        self.key = MOVIEDB_API_KEY
        self.key_text = 'api_key'
        self.base = MOVIEDB_API_BASE
        self.search = MOVIEDB_API_SEARCH
        self.region = MOVIEDB_API_REGION
        self.region_text = 'region'
        self.lang_text = 'language'
        self.lang = MOVIEDB_API_LANG
        self.query_delim = '?'
        self.param_delim = '&'
        self.query = None
        self.query_text = 'query'

class SearchResultGetter(MovieDBResults):
    """get search results using external API"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_search_results(self):
        """hit external api and get results"""
        assert len(self.request.query_params['query']) <= 30, \
                "Search query cannot be greater than 30 characters"
        self.query = self.request.query_params['query']
        api_endpoint = '{}/{}'.format(self.base, self.search)
        api_endpoint = SearchResultGetter._add_request_param(api_endpoint, self.key,\
                self.key_text, self.query_delim)
        api_endpoint = SearchResultGetter._add_request_param(api_endpoint, self.lang,\
                self.lang_text, self.param_delim)
        api_endpoint = SearchResultGetter._add_request_param(api_endpoint, self.region,\
                self.region_text, self.param_delim)
        api_endpoint = SearchResultGetter._add_request_param(api_endpoint, self.query,\
                self.query_text, self.param_delim)
        LOGGER.info("API ENDPOINT: %s", api_endpoint)
        data = requests.get(api_endpoint).json()
        return data # pragma: no cover

    @staticmethod
    def _add_request_param(resource, key, param, delim):
        """add key to resource identifier"""
        assert param is not None, "param cannot be None"
        return '{}{}{}={}'.format(resource, delim, param, key)
