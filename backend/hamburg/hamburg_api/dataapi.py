"""Business Logic Layer"""

import logging
from datetime import datetime, timedelta
from django.db.models import Q
import requests
from hamburg.settings import MOVIEDB_API_KEY,\
        MOVIEDB_API_SEARCH, MOVIEDB_API_BASE, MOVIEDB_API_REGION,\
        MOVIEDB_API_LANG, ALERT_THRESHOLD, MOVIEDB_API_DETAILS,\
        MOVIEDB_API_VIDEO, MOVIEDB_API_SHOWTIMES, MOVIEDB_API_UPCOMING,\
        MOVIEDB_API_POPULAR, MOVIEDB_API_POPULAR, MOVIEDB_API_NOW_PLAYING,\
        MOVIEDB_API_SIMILAR, MOVIEDB_API_RECO
from .models import EmailAlertModel

LOGGER = logging.getLogger(__name__)

class MovieDBResults():
    """Class for all data related to MovieDB"""

    QUERY_DELIM = '?'
    PARAM_DELIM = '&'

    def __init__(self):
        self.key = MOVIEDB_API_KEY
        self.key_text = 'api_key'
        self.base = MOVIEDB_API_BASE
        self.search = MOVIEDB_API_SEARCH
        self.region = MOVIEDB_API_REGION
        self.region_text = 'region'
        self.lang_text = 'language'
        self.lang = MOVIEDB_API_LANG
        self.query = None
        self.query_text = 'query'
        self.details = MOVIEDB_API_DETAILS
        self.showtime = MOVIEDB_API_SHOWTIMES
        self.video = MOVIEDB_API_VIDEO
        self.upcoming = MOVIEDB_API_UPCOMING
        self.popular = MOVIEDB_API_POPULAR
        self.now_playing = MOVIEDB_API_NOW_PLAYING
        self.similar = MOVIEDB_API_SIMILAR
        self.reco = MOVIEDB_API_RECO

    @staticmethod
    def add_request_param(resource, key, param, delim):
        """add key to resource identifier"""
        assert param is not None, "param cannot be None"
        return '{}{}{}={}'.format(resource, delim, param, key)


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
        return SimpleGetter.get_simple(self.base, self.search, self.key, self.key_text,\
                    self.lang, self.lang_text, self.region, self.region_text, query=self.query,\
                    query_text=self.query_text)


class EmailAlertCreater():
    """Class to create email alerts"""
    def __init__(self, request):
        self.request = request
        self.data = None

    def _create_model_data_dict(self):
        """Helper method to encapsulate data to be saved"""
        data_dict = {}
        data_dict['email'] = self.data['email']
        data_dict['movie_name'] = self.data['movie_name']
        data_dict['release_date'] = self.data['release_date']
        data_dict['alert_date'] = self.data.get('alert_date')
        return data_dict

    def save_alert_request(self):
        "save alert request in the backend db"""
        self.data = self.request.data
        data_dict = self._create_model_data_dict()
        alert = EmailAlertModel(**data_dict)
        alert.save()
        return {'saved': True}


class DataGetter():
    """Data getter class"""

    @staticmethod
    def get_email_alert_data(values=None):
        """get data from email_alert table"""
        if values is None:
            values = ['id', 'movie_name', 'email']
        today = datetime.today().date()
        till = today + timedelta(ALERT_THRESHOLD)
        alter_bool = Q(alert_date__isnull=False)
        alert_cond = Q(alert_date=today)
        release_lower = Q(release_date__gte=today)
        release_upper = Q(release_date__lte=till)
        dataset = EmailAlertModel.objects.filter((alter_bool & alert_cond)\
                | (release_upper & release_lower)).values(*values)
        return dataset


class MovieDetailsGetter(MovieDBResults):
    """get movie details useing external API"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_movie_details(self):
        """get movie details"""
        self.query = self.request.query_params['query']
        self.details = self.details.format(self.query)
        return SimpleGetter.get_simple(self.base, self.details, self.key, self.key_text,\
                    self.lang, self.lang_text, self.region, self.region_text)


class ShowtimeDetailsGetter(MovieDBResults):
    """get showtimes details useing external API"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_showtime_details(self):
        """get showtime details"""
        return {}


class MovieTrailerGetter(MovieDBResults):
    """get showtimes details useing external API"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_movie_trailer(self):
        """get movie trailer"""
        self.query = self.request.query_params['query']
        self.video = self.video.format(self.query)
        data = SimpleGetter.get_simple(self.base, self.video, self.key, self.key_text,\
                    self.lang, self.lang_text, self.region, self.region_text)
        filtered = list(filter(lambda x: "Trailer" in x.values(),\
                data['results']))
        if filtered:
            return {'video': filtered[0]['key']}
        filtered = list(filter(lambda x: "Teaser" in x.values(),\
                data['results']))
        if filtered:
            return {'video': filtered[0]['key']}
        return {'video': None} # pragma: no cover


class UpcomingDetailsGetter(MovieDBResults):
    """get upcoming movie details useing external API"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_upcoming_details(self):
        """get upcoming details"""
        return SimpleGetter.get_simple(self.base, self.upcoming, self.key, self.key_text,\
                    self.lang, self.lang_text, self.region, self.region_text)


class PopularDetailsGetter(MovieDBResults):
    """get popular movie details useing external API"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_popular_details(self):
        """get popular details"""
        return SimpleGetter.get_simple(self.base, self.popular, self.key, self.key_text,\
                    self.lang, self.lang_text, self.region, self.region_text)


class NowPlayingDetailsGetter(MovieDBResults):
    """get now playing details useing external API"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_now_playing_details(self):
        """get now playing details"""
        return SimpleGetter.get_simple(self.base, self.now_playing, self.key, self.key_text,\
                    self.lang, self.lang_text, self.region, self.region_text)


class SimilarDetailsGetter(MovieDBResults):
    """get details for similar movies"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_similar_movies(self):
        """get movie trailer"""
        self.query = self.request.query_params['query']
        self.similar = self.similar.format(self.query)
        return SimpleGetter.get_simple(self.base, self.similar, self.key, self.key_text,\
                    self.lang, self.lang_text, self.region, self.region_text)


class RecoDetailsGetter(MovieDBResults):
    """get details for recommended movies"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_recommended_movies(self):
        """get movie trailer"""
        self.query = self.request.query_params['query']
        self.reco = self.reco.format(self.query)
        return SimpleGetter.get_simple(self.base, self.reco, self.key, self.key_text,\
                    self.lang, self.lang_text, self.region, self.region_text)


class SimpleGetter():
    """Simple get request"""
    @staticmethod
    def get_simple(base, resource, key, key_text, lang, lang_text,\
            region, region_text, query=None, query_text=None):
        """simple get requests"""
        api_endpoint = '{}/{}'.format(base, resource)
        api_endpoint = MovieDBResults.add_request_param(api_endpoint, key,\
                key_text, MovieDBResults.QUERY_DELIM)
        api_endpoint = MovieDBResults.add_request_param(api_endpoint, lang,\
                lang_text, MovieDBResults.PARAM_DELIM)
        api_endpoint = MovieDBResults.add_request_param(api_endpoint, region,\
                region_text, MovieDBResults.PARAM_DELIM)
        if query is not None:
            api_endpoint = MovieDBResults.add_request_param(api_endpoint, query,\
                    query_text, MovieDBResults.PARAM_DELIM)
        LOGGER.info("API ENDPOINT: %s", api_endpoint)
        data = requests.get(api_endpoint).json()
        return data # pragma: no cover
