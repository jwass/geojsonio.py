#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import json
import sys
import urllib
import webbrowser

import github3

MAX_URL_LEN = 150e3  # Size threshold above which a gist is created


def display(contents, domain='http://geojson.io/', force_gist=False):
    url = geojsonio_url(contents, domain, force_gist)
    webbrowser.open(url)
    return url
# display() used to be called to_geojsonio. Keep it around for now...
to_geojsonio = display


def geojsonio_url(contents, domain='http://geojson.io/', force_gist=False):
    """
    Returns the URL to open given the domain and contents

    The input contents may be:
    * string - assumed to be GeoJSON
    * an object that implements __geo_interface__
        A FeatureCollection will be constructed with one feature,
        the object.
    * a sequence of objects that each implement __geo_interface__
        A FeatureCollection will be constructed with the objects
        as the features

    For more information about __geo_interface__ see:
    https://gist.github.com/sgillies/2217756

    If the contents are large, then a gist will be created.

    """
    contents = _parse_contents(contents)
    if len(contents) <= MAX_URL_LEN and not force_gist:
        url = _data_url(domain, contents)
    else:
        gist = _create_gist(contents)
        url = _gist_url(domain, gist.id)

    return url


def _parse_contents(contents):
    """
    Return a GeoJSON string from a variety of inputs.
    See the documentation for geojsonio_url for the possible contents
    input.

    Returns
    -------
    GeoJSON string

    """
    if isinstance(contents, basestring):
        return contents

    if hasattr(contents, '__geo_interface__'):
        features = [_geo_to_feature(contents)]
    else:
        try:
            feature_iter = iter(contents)
        except TypeError:
            raise ValueError('Unknown type for input')

        features = []
        for i, f in enumerate(feature_iter):
            if not hasattr(f, '__geo_interface__'):
                raise ValueError('Unknown type at index {}'.format(i))
            features.append(_geo_to_feature(f))

    data = {'type': 'FeatureCollection', 'features': features}
    return json.dumps(data)


def _geo_to_feature(ob):
    """
    Return a GeoJSON Feature from an object that implements
    __geo_interface__

    If the object's type is a geometry, return a Feature with empty
    properties and the object's mapping as the feature geometry. If the
    object's type is a Feature, then return it.

    """
    mapping = ob.__geo_interface__
    if mapping['type'] == 'Feature':
        return mapping
    else:
        return {'type': 'Feature',
                'geometry': mapping}


def _create_gist(contents, description='', filename='data.geojson'):
    """
    Create and return an anonymous gist with a single file and specified
    contents

    """
    ghapi = github3.GitHub()
    files = {filename: {'content': contents}}
    gist = ghapi.create_gist(description, files)

    return gist


def _data_url(domain, contents):
    url = (domain + '#data=data:application/json,' +
           urllib.quote(contents))
    return url


def _gist_url(domain, gist_id):
    url = (domain + '#id=gist:/{}'.format(gist_id))
    return url


def main():
    parser = argparse.ArgumentParser(
        description='Quickly visualize GeoJSON data on geojson.io')

    parser.add_argument('-p', '--print',
                        dest='do_print',
                        action='store_true',
                        help='print the URL')

    parser.add_argument('-d', '--domain',
                        dest='domain',
                        default='http://geojson.io',
                        help='Alternate URL instead of http://geojson.io/')

    parser.add_argument('filename',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="The file to send to geojson.io")

    args = parser.parse_args()

    contents = args.filename.read()
    url = geojsonio_url(contents, args.domain)
    if args.do_print:
        print(url)
    else:
        webbrowser.open(url)

if __name__ == '__main__':
    main()
