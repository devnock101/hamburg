"""Business Logic Layer"""

import logging
from datetime import datetime, timedelta
from django.db.models import Q
import requests
from hamburg.settings import MOVIEDB_API_KEY,\
        MOVIEDB_API_SEARCH, MOVIEDB_API_BASE, MOVIEDB_API_REGION,\
        MOVIEDB_API_LANG, ALERT_THRESHOLD, MOVIEDB_API_DETAILS,\
        MOVIEDB_API_VIDEO, MOVIEDB_API_SHOWTIME
from .models import EmailAlertModel

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
        self.details = MOVIEDB_API_DETAILS
        self.showtime = MOVIEDB_API_SHOWTIME
        self.video = MOVIEDB_API_VIDEO

    @staticmethod
    def _add_request_param(resource, key, param, delim):
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
        api_endpoint = '{}/{}'.format(self.base, self.details)
        api_endpoint = MovieDetailsGetter._add_request_param(api_endpoint, self.key,\
                self.key_text, self.query_delim)
        api_endpoint = MovieDetailsGetter._add_request_param(api_endpoint, self.lang,\
                self.lang_text, self.param_delim)
        self._get_trailer_path()
        return {}

    def _get_trailer_path(self):
        """get movie trailer path"""
        self.video = self.video.format(self.query)
        api_endpoint = '{}/{}'.format(self.base, self.video)
        return ""


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
        return {}
