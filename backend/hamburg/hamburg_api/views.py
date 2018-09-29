"""View Layer"""

import traceback
import sys
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from .dataapi import SearchResultGetter


class SearchView(APIView):
    """Welcome/Test View"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['get']

    @staticmethod
    def get(request):
        """get results based on the search parameter"""
        try:
            response = SearchResultGetter(request).get_search_results()
            return Response(response) # pragma: no cover
        #pylint: disable=broad-except
        except Exception:
            _exc_type, _exc_valye, exc_traceback = sys.exc_info()
            return Response(traceback.format_tb(exc_traceback), status=500)
