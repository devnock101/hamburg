"""collection of decorators used"""

import sys
import functools
import traceback
from rest_framework.response import Response

def error_decorator(func):
    """error decorator for API calls"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        #pylint: disable=broad-except
        except Exception:
            _exc_type, _exc_value, exc_traceback = sys.exc_info()
            response = {}
            response['errors'] = traceback.format_tb(exc_traceback)
            response['saved'] = False
            return Response(response, status=500)
    return wrapper
