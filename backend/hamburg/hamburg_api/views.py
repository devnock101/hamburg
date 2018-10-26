"""View Layer"""

from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from .dataapi import SearchResultGetter, EmailAlertCreater,\
        DataGetter, ShowtimeDetailsGetter, MovieDetailsGetter
from .decorators import error_decorator


class SearchView(APIView):
    """Search View"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['get']

    @staticmethod
    @error_decorator
    def get(request):
        """get results based on the search parameter"""
        response = SearchResultGetter(request).get_search_results()
        return Response(response) # pragma: no cover


class EmailAlertView(APIView):
    """View to create email alters based on input email"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['post']

    @staticmethod
    @error_decorator
    def post(request):
        """save an alert request"""
        response = EmailAlertCreater(request).save_alert_request()
        return Response(response) # pragma: no cover


class ScheduleRunView(APIView):
    """View to run scheduled jobs"""
    http_method_names = ['post']

    @staticmethod
    @error_decorator
    def post(_request):
        """run a scheduled job"""
        response = DataGetter.get_email_alert_data()
        return Response(response) # pragma: no cover


class MovieDetailsView(APIView):
    """Movie Details View"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['get']

    @staticmethod
    @error_decorator
    def get(request):
        """get results based on the search parameter"""
        response = MovieDetailsGetter(request).get_movie_details()
        return Response(response) # pragma: no cover


class ShowtimeDetailsView(APIView):
    """Showtime Details View"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['get']

    @staticmethod
    @error_decorator
    def get(request):
        """get results based on the search parameter"""
        response = ShowtimeDetailsGetter(request).get_showtime_details()
        return Response(response) # pragma: no cover
