"""View Layer"""

import traceback
import sys
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from .dataapi import SearchResultGetter, EmailAlertCreater,\
        DataGetter


class SearchView(APIView):
    """Search View"""
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
            _exc_type, _exc_value, exc_traceback = sys.exc_info()
            return Response(traceback.format_tb(exc_traceback), status=500)


class EmailAlertView(APIView):
    """View to create email alters based on input email"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['post']

    @staticmethod
    def post(request):
        """save an alert request"""
        response = {}
        try:
            response = EmailAlertCreater(request).save_alert_request()
            return Response(response) # pragma: no cover
        #pylint: disable=broad-except
        except Exception:
            _exc_type, _exc_value, exc_traceback = sys.exc_info()
            response['errors'] = traceback.format_tb(exc_traceback)
            response['saved'] = False
            return Response(response, status=500)


class ScheduleRunView(APIView):
    """View to run scheduled jobs"""
    http_method_names = ['post']

    @staticmethod
    def post(_request):
        """run a scheduled job"""
        response = {}
        try:
            response = DataGetter.get_email_alert_data()
            return Response(response) # pragma: no cover
        #pylint: disable=broad-except
        except Exception:
            _exc_type, _exc_value, exc_traceback = sys.exc_info()
            response['errors'] = traceback.format_tb(exc_traceback)
            return Response(response, status=500)
