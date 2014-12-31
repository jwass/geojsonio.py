from __future__ import unicode_literals

import json
from six.moves import urllib

import geojsonio
import github3

import mock
import pytest


@pytest.fixture
def features():
    feat1 = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [1.0, 2.0],
        },
        'properties': {
            'prop1': 'value1',
            'prop2': 2.0,
        }
    }
    feat2 = {
        'type': 'Feature',
        'geometry': {
            'type': 'LineString',
            'coordinates': [[3.0, 4.0], [5.0, 6.0]],
        },
        'properties': {
            'prop1': 'lineval',
            'prop2': 3.0,
        }
    }

    fc = {
        'type': 'FeatureCollection',
        'features': [feat1, feat2],
    }

    return fc


class GeoDict(object):
    """
    Simple class providing __geo_interface__ on geojson-like dicts

    """
    def __init__(self, d):
        self.d = d

    @property
    def __geo_interface__(self):
        return self.d


def test_parse_string(features):
    contents = json.dumps(features)

    assert geojsonio.make_geojson(contents) == contents


def test_parse_single_feature_geo(features):
    feature = features['features'][0]
    o = GeoDict(feature)

    expected = {
        'type': 'FeatureCollection',
        'features': [feature]
    }

    contents = geojsonio.make_geojson(o)
    assert contents == json.dumps(expected)


def test_parse_list_features_geo(features):
    os = [GeoDict(f) for f in features['features']]
    contents = geojsonio.make_geojson(os)

    dict_contents = json.loads(contents)
    assert features == dict_contents


def test_parse_fail_non_feature():
    with pytest.raises(ValueError):
        geojsonio.make_geojson(5)


def test_parse_fail_list_non_feature(features):
    os = [GeoDict(features['features'][0]), 5]
    with pytest.raises(ValueError):
        geojsonio.make_geojson(os)


def test_data_url(features):
    feature = features['features'][0]
    header = "http://geojson.io/#data=data:application/json,"
    length = len(header)

    result = geojsonio.data_url(json.dumps(feature))
    payload = json.loads(urllib.parse.unquote(result[length:]))

    assert result[:length] == header
    assert payload == feature


def test_gist_url():
    expected = "http://geojson.io/#id=gist:/abcd"

    assert expected == geojsonio.gist_url('abcd')


def test_factory_data(features):
    contents = json.dumps(features)
    size = len(contents)

    url = geojsonio.make_url(contents, size_for_gist=size+1)
    assert url == geojsonio.data_url(contents)


def test_factory_gist(features):
    contents = json.dumps(features)
    size = len(contents)

    with mock.patch.object(github3.GitHub, 'create_gist') as MockInstance:
        class Dummy(object):
            id = 'abc123'
        MockInstance.return_value = Dummy()
        url = geojsonio.make_url(contents, size_for_gist=size-1)

    assert url == geojsonio.gist_url(Dummy.id)


def test_factory_force_gist(features):
    contents = json.dumps(features)
    size = len(contents)

    with mock.patch.object(github3.GitHub, 'create_gist') as MockInstance:
        class Dummy(object):
            id = 'abc123'
        MockInstance.return_value = Dummy()
        url = geojsonio.make_url(contents, size_for_gist=size+1,
                                 force_gist=True)

    assert url == geojsonio.gist_url(Dummy.id)
