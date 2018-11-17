"""View Layer"""

from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from .dataapi import SearchResultGetter, EmailAlertCreater,\
        DataGetter, ShowtimeDetailsGetter, MovieDetailsGetter,\
        UpcomingDetailsGetter, PopularDetailsGetter,\
        NowPlayingDetailsGetter, MovieTrailerGetter,\
        SimilarDetailsGetter, RecoDetailsGetter,\
        ExploreDataGetter
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
        response_details = MovieDetailsGetter(request).get_movie_details()
        response_video = MovieTrailerGetter(request).get_movie_trailer()
        response_details.update(response_video)
        return Response(response_details) # pragma: no cover


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


class UpcomingView(APIView):
    """Upcoming Movies"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['get']

    @staticmethod
    @error_decorator
    def get(request):
        """get results based on the search parameter"""
        response = UpcomingDetailsGetter(request).get_upcoming_details()
        return Response(response) # pragma: no cover


class PopularView(APIView):
    """Popular Movies View"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['get']

    @staticmethod
    @error_decorator
    def get(request):
        """get results based on the search parameter"""
        response = PopularDetailsGetter(request).get_popular_details()
        return Response(response) # pragma: no cover


class NowPlayingView(APIView):
    """Now playing movies"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['get']

    @staticmethod
    @error_decorator
    def get(request):
        """get results based on the search parameter"""
        response = NowPlayingDetailsGetter(request).get_now_playing_details()
        return Response(response) # pragma: no cover


class SimilarView(APIView):
    """Now playing movies"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['get']

    @staticmethod
    @error_decorator
    def get(request):
        """get results based on the search parameter"""
        response = SimilarDetailsGetter(request).get_similar_movies()
        return Response(response) # pragma: no cover


class RecommendedView(APIView):
    """Now playing movies"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['get']

    @staticmethod
    @error_decorator
    def get(request):
        """get results based on the search parameter"""
        response = RecoDetailsGetter(request).get_recommended_movies()
        return Response(response) # pragma: no cover


class ExploreView(APIView):
    """Explore Movie"""
    throttle_classes = (UserRateThrottle,)
    http_method_names = ['get']

    @staticmethod
    @error_decorator
    def get(request):
        """get results based on the search parameter"""
        response = ExploreDataGetter(request).get_explore_data()
        return Response(response) # pragma: no cover
