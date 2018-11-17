"""Business Logic Layer"""

import logging
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import IntegrityError, ProgrammingError
from django.forms.models import model_to_dict
import requests
from hamburg.settings import MOVIEDB_API_KEY,\
        MOVIEDB_API_SEARCH, MOVIEDB_API_BASE, MOVIEDB_API_REGION,\
        MOVIEDB_API_LANG, ALERT_THRESHOLD, MOVIEDB_API_DETAILS,\
        MOVIEDB_API_VIDEO, MOVIEDB_API_SHOWTIMES, MOVIEDB_API_UPCOMING,\
        MOVIEDB_API_POPULAR, MOVIEDB_API_NOW_PLAYING,\
        MOVIEDB_API_SIMILAR, MOVIEDB_API_RECO, MOVIEGLU_API_BASE,\
        MOVIEGLU_API_CLIENT, MOVIEGLU_API_KEY, MOVIEGLU_API_AUTH,\
        MOVIEGLU_API_VERSION, MOVIEGLU_API_TERRITORY, MOVIEGLU_API_SEARCH,\
        MOVIEGLU_API_GEO, MOVIEGLU_API_SHOWTIME, MOVIEDB_API_KEYWORDS,\
        MOVIEDB_API_CREDITS
from .models import EmailAlertModel, MovieIdMapperModel

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
        self.imdb_id = None
        self.movie_name = None
        self.movieglu_headers = {\
                'client': MOVIEGLU_API_CLIENT,\
                'territory': MOVIEGLU_API_TERRITORY,\
                'api-version': MOVIEGLU_API_VERSION,\
                'authorization': MOVIEGLU_API_AUTH,\
                'device-datetime': datetime.now().isoformat(),\
                'x-api-key': MOVIEGLU_API_KEY,
                'geolocation': MOVIEGLU_API_GEO
                }
        self.movieglu_base = MOVIEGLU_API_BASE
        self.movieglu_search = MOVIEGLU_API_SEARCH
        self.movieglu_showtimes = MOVIEGLU_API_SHOWTIME
        self.movieglu_query_text = "film_id"
        self.results_key = 'results'
        self.keywords = MOVIEDB_API_KEYWORDS
        self.credits = MOVIEDB_API_CREDITS

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
                    language="en-US", region="US", query=self.query)


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
            values = ['id', 'movie_name', 'email', 'done', 'release_date']
        today = datetime.today().date()
        till = today + timedelta(ALERT_THRESHOLD)
        not_done = Q(done=False)
        _alter_bool = Q(alert_date__isnull=False)
        _alert_cond = Q(alert_date=today)
        _release_lower = Q(release_date__gte=today)
        _release_upper = Q(release_date__lte=till)
        # dataset = EmailAlertModel.objects.filter((alter_bool & alert_cond)\
        #         | (release_upper & release_lower)).values(*values)
        dataset = EmailAlertModel.objects.filter(not_done).\
                values(*values)
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
                    language="en-US", region="US")


class ShowtimeDetailsGetter(MovieDBResults):
    """get showtimes details useing external API"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_showtime_details(self):
        """get showtime details"""
        self.query = self.request.query_params['query']
        self.imdb_id = self.request.query_params['imdb_id']
        self.movie_name = self.request.query_params['movie_name']
        mapping = False
        try:
            mapping = model_to_dict(\
                    MovieIdMapperModel.objects.get(moviedb_id=self.query))
        except MultipleObjectsReturned as exception:
            LOGGER.info("MultipleObjectsReturned")
            LOGGER.info(exception)
            return {"errors": "Showtimes not found"}
        except ObjectDoesNotExist as exception:
            LOGGER.info("ObjectDoesNotExist")
            LOGGER.info(exception)
            try:
                mapping = self._create_mapping()
                MovieIdMapperModel(**mapping).save()
            except IntegrityError as i_error:
                LOGGER.info(i_error)
                return {"errors": "Showtimes not found"}
        except ProgrammingError as prog_error:
            LOGGER.info(prog_error)
            return {"errors": "Showtimes not found"}
        return SimpleGetter.get_simple(self.movieglu_base, self.movieglu_showtimes,\
                    mapping['movieglu_id'], self.movieglu_query_text,\
                    date=str(datetime.today().date()), n=25, headers=self.movieglu_headers)

    def _create_mapping(self):
        """create moviedb and movieglu id mapping"""
        data = SimpleGetter.get_simple(self.movieglu_base, self.movieglu_search,\
                    self.movie_name, self.query_text, n=15, headers=self.movieglu_headers)
        rtr = None
        films = data.get('films')
        if films is None:
            return {'moviedb_id': self.query, 'movieglu_id': rtr, 'imdb_id': self.imdb_id}
        for film in films:
            if film['imdb_id'] == int(self.imdb_id[2:]): # moviedb imdbid begins with 'tt'
                rtr = film['film_id']
                break
        return {'moviedb_id': self.query, 'movieglu_id': rtr, 'imdb_id': self.imdb_id}


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
                    language="en-US", region="US")
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
                    language="en-US", region="US")


class PopularDetailsGetter(MovieDBResults):
    """get popular movie details useing external API"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_popular_details(self):
        """get popular details"""
        return SimpleGetter.get_simple(self.base, self.popular, self.key, self.key_text,\
                    language="en-US", region="US")


class NowPlayingDetailsGetter(MovieDBResults):
    """get now playing details useing external API"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_now_playing_details(self):
        """get now playing details"""
        return SimpleGetter.get_simple(self.base, self.now_playing, self.key, self.key_text,\
                    language="en-US", region="US")


class SimilarDetailsGetter(MovieDBResults):
    """get details for similar movies"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_similar_movies(self):
        """get movie trailer"""
        self.query = self.request.query_params['query']
        self.similar = self.similar.format(self.query)
        similar = SimpleGetter.get_simple(self.base, self.similar, self.key, self.key_text,\
                    language="en-US", region="US")
        similar[self.results_key] = Rank.get_ranked(similar[self.results_key])
        return similar


class RecoDetailsGetter(MovieDBResults):
    """get details for recommended movies"""
    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_recommended_movies(self):
        """get movie trailer"""
        self.query = self.request.query_params['query']
        self.reco = self.reco.format(self.query)
        reco = SimpleGetter.get_simple(self.base, self.reco, self.key, self.key_text,\
                    language="en-US", region="US")
        reco[self.results_key] = Rank.get_ranked(reco[self.results_key])
        return reco


class SimpleGetter():
    """Simple get request"""
    @staticmethod
    def get_simple(base, resource, key, key_text, **kwargs):
        """simple get requests"""
        api_endpoint = '{}/{}'.format(base, resource)
        api_endpoint = MovieDBResults.add_request_param(api_endpoint, key,\
                key_text, MovieDBResults.QUERY_DELIM)
        try:
            headers = kwargs.pop("headers")
        except KeyError as _key_error:
            headers = None
        for _key, value in kwargs.items():
            api_endpoint = MovieDBResults.add_request_param(api_endpoint, value,\
                _key, MovieDBResults.PARAM_DELIM)
        LOGGER.info("API ENDPOINT: %s", api_endpoint)
        data = requests.get(api_endpoint, headers=headers).json()
        return data # pragma: no cover


class Rank():
    """Rank a list of movies"""

    @staticmethod
    def get_ranked(data):
        """get ranked data"""
        return sorted(data, key=lambda x: (x['release_date'],\
                x['popularity'], x['vote_count']), reverse=True)


class MovieDBKeywordGetter(MovieDBResults):
    """get keywords associated with a movie"""

    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_keywords(self):
        """get keywords"""
        self.query = self.request.query_params['query']
        self.keywords = self.keywords.format(self.query)
        return SimpleGetter.get_simple(self.base, self.keywords, self.key, self.key_text,\
                    language="en-US", region="US")


class CreditsGetter(MovieDBResults):
    """get credits associated with a movie"""

    def __init__(self, request):
        super().__init__()
        self.request = request

    def get_credits(self):
        """get credits"""
        self.query = self.request.query_params['query']
        self.credits = self.credits.format(self.query)
        return SimpleGetter.get_simple(self.base, self.credits, self.key, self.key_text,\
                    language="en-US", region="US")


class ExploreDataGetter(MovieDBResults):
    """ExploreMovie Data"""

    def __init__(self, request):
        super().__init__()
        self.request = request
        self.data = {}

    @staticmethod
    def _process(data):
        """process data"""
        data['credit'] = ExploreDataGetter._process_credits(\
                data['credit']['cast'])
        data['keywords'] = ExploreDataGetter._process_keywords(\
                data['keywords']['keywords'])
        data['reco'] = ExploreDataGetter._process_reco(\
                data['reco']['results'])
        data['similar'] = ExploreDataGetter._process_similar(\
                data['similar']['results'])
        data['genres'] = ExploreDataGetter._process_genres(\
                data['details']['genres'])
        data['details'] = ExploreDataGetter._process_details(\
                data['details'])
        return data

    @staticmethod
    def _process_details(data):
        """extract details"""
        return {'name': data.get('overview'), 'status': data.get('status'),\
                'tagline': data.get('tagline'),\
                'runtime': str(timedelta(minutes=data.get('runtime'))),\
                'popularity': data.get('popularity'), 'vote_count': data.get('vote_count'),\
                'vote_avg': data.get('vote_average')}

    @staticmethod
    def _process_genres(data):
        """extract genre"""
        return [{'name': x['name']} for x in data]

    @staticmethod
    def _process_credits(data):
        """extract credits"""
        data = sorted(data, key=lambda x: x['cast_id'])
        data = data[:5] # get top 5
        return [{'name': x['name'], 'character': x['character'], 'img': x['profile_path']}\
                for x in data]

    @staticmethod
    def _process_reco(data):
        """extract reco"""
        data = data[:5] # get top 5, already sorted list
        return [{'name': x['title'], 'img': x['poster_path']} for x in data]

    @staticmethod
    def _process_similar(data):
        """extract similar"""
        data = data[:5] # get top 5, already sorted list
        return [{'name': x['title'], 'img': x['poster_path']}\
                for x in data]

    @staticmethod
    def _process_keywords(data):
        """extract keywords"""
        return [{'name': x['name']} for x in data]

    def get_explore_data(self):
        """get explore data"""
        self.data['details'] = MovieDetailsGetter(self.request).get_movie_details()
        self.data['similar'] = SimilarDetailsGetter(self.request).get_similar_movies()
        self.data['reco'] = RecoDetailsGetter(self.request).get_recommended_movies()
        self.data['credit'] = CreditsGetter(self.request).get_credits()
        self.data['keywords'] = MovieDBKeywordGetter(self.request).get_keywords()
        self.data['genres'] = None # filled while processing
        self.data = ExploreDataGetter._process(self.data)
        return self.data
