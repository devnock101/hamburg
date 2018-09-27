"""Test cases for the views module"""

import json
import requests
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from hamburg_api.views import SearchView
from .constants import MOCK_SEARCH_API


class TestSearchView():
    """Test class of SearchView"""

    @staticmethod
    def test_get(monkeypatch):
        """test method for get request"""
        factory = APIRequestFactory()
        def mockreturn(_endpoint):
            res = requests.Response()
            #pylint: disable=protected-access
            res._content = bytes(json.dumps(MOCK_SEARCH_API),\
                    encoding='utf-8')
            return res
        monkeypatch.setattr(requests, 'get', mockreturn)
        request = factory.get('/api/v1/moviedb/search/', data={'query': 'venom'})
        request = APIView().initialize_request(request)
        view = SearchView()
        response = view.get(request)
        assert response.status_code == 200

    @staticmethod
    def test_get_error(monkeypatch):
        """test method for get request"""
        factory = APIRequestFactory()
        def mockreturn(_endpoint):
            return None
        monkeypatch.setattr(requests, 'get', mockreturn)
        request = factory.get('/api/v1/moviedb/search/', data={'query': 'venom'})
        request = APIView().initialize_request(request)
        view = SearchView()
        response = view.get(request)
        assert response.status_code == 500
