"""MovieDB Data Fetching Script"""

from urllib import request
#from pdb import set_trace as st
from collections import namedtuple
import os
import time
import json
import pickle

# https://api.themoviedb.org/3/movie/upcoming?api_key=&language=en-US&page=3&region=US

def get_api_rate(xrl):
    """get api hit rate based on server rate limiting"""
    new_count = 0
    new_time = 0
    if xrl.unit == 'S':
        rate = xrl.count / xrl.time
        assert rate > 0, "X-RATE cannot be negative"
        if rate == 1:
            new_count = rate
            new_time = 1
        elif rate > 1:
            new_count = rate - 1
            new_time = 1
        else:
            while rate < 1:
                rate *= 10
            new_count = 1
            new_time = int(xrl.rate)
        return (new_count, new_time)
    return (new_count, new_time)

def add_request_param(resource, key, param=None, delim='&'):
    """add key to resource identifier"""
    assert param is not None, "param cannot be None"
    return '{}{}{}={}'.format(resource, delim, param, key)

def get_data(end_point, xrl, base_url=None, api_key=None, pages=1):
    """get the release dates and details of upcoming movies in theaters"""
    assert base_url is not None, "BASE_URL cannot be None"
    assert api_key is not None, "API_KEY cannot be None"
    assert pages is not None, "Number of pages cannot be None"
    api_endpoint = '{}/{}'.format(base_url, end_point)
    api_endpoint = add_request_param(api_endpoint, api_key, 'api_key', '?')
    api_endpoint = add_request_param(api_endpoint, 'en-US', 'language')
    api_endpoint = add_request_param(api_endpoint, 'US', 'region')
    xrl = get_api_rate(xrl)
    print(xrl)
    print('API rate is: {} requests in {} seconds'.format(xrl[0], xrl[1]))
    while pages > 0:
        final_endpoint = add_request_param(api_endpoint, pages, 'page')
        print('Requesting: {}'.format(final_endpoint))
        pages -= 1
        data = json.loads(request.urlopen(api_endpoint).read().decode('utf-8'))
        pickle.dump(data, open('{}_{}'.format(end_point, pages), 'wb'),\
                protocol=pickle.HIGHEST_PROTOCOL)
        time.sleep(xrl[1] / xrl[0])

if __name__ == '__main__':
    API_KEY = os.environ['MOVIEDB_API_KEY']
    BASE_URL = "https://api.themoviedb.org/3/movie"
    UPCOMING_ENDPOINT = 'upcoming'
    NOW_PLAYING_ENDPOINT = 'now_playing'
    UPCOMING_PAGES = 4
    NOW_PLAYING_PAGES = 57
    XRateLimit = namedtuple('XRateLimit', ['count', 'time', 'unit'])
    XRL = XRateLimit(40, 10, 'S')
    get_data(UPCOMING_ENDPOINT, XRL, BASE_URL, API_KEY, UPCOMING_PAGES)
    get_data(NOW_PLAYING_ENDPOINT, XRL, BASE_URL, API_KEY, NOW_PLAYING_PAGES)
