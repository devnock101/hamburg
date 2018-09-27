"""Test cases for the dataapi module"""

import pytest
from hamburg_api.dataapi import SearchResultGetter

class TestSearchResultGetter():
    """Test class for SearchResultGetter"""

    testdata = [
        ("https://my-app/api/v1/", "my-first-value",\
                "my-first-key", "&",\
                "https://my-app/api/v1/&my-first-key=my-first-value"),
        ("https://my-app/api/v1/", "my-second-value",\
                "my-second-key", "?",\
                "https://my-app/api/v1/?my-second-key=my-second-value"),
    ]
    @staticmethod
    @pytest.mark.parametrize("resource, key, param, delim, expected", testdata)
    def test__add_request_param(resource, key, param, delim, expected):
        """test method for _add_request_param"""
        #pylint: disable=protected-access
        assert SearchResultGetter._add_request_param(resource, key, param, delim) == expected
