#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import json
import sys
import webbrowser

import github3
import six
from six.moves import urllib

MAX_URL_LEN = 150e3  # Size threshold above which a gist is created
DEFAULT_DOMAIN = 'http://geojson.io/'


def display(contents, domain=DEFAULT_DOMAIN, force_gist=False):
    """
    Open a web browser pointing to geojson.io with the specified content.

    If the content is large, an anonymous gist will be created on github and
    the URL will instruct geojson.io to download the gist data and then
    display. If the content is small, this step is not needed as the data can
    be included in the URL

    Parameters
    ----------
    content - (see make_geojson)
    domain - string, default http://geojson.io
    force_gist - bool, default False
        Create an anonymous gist on Github regardless of the size of the
        contents

    """
    url = make_url(contents, domain, force_gist)
    webbrowser.open(url)
    return url
# display() used to be called to_geojsonio. Keep it around for now...
to_geojsonio = display


def embed(contents='', width='100%', height=512, *args, **kwargs):
    """
    Embed geojson.io in an iframe in Jupyter/IPython notebook.

    Parameters
    ----------
    contents - see make_url()
    width - string, default '100%' - width of the iframe
    height - string / int, default 512 - height of the iframe
    kwargs - additional arguments are passed to `make_url()`

    """
    from IPython.display import HTML

    url = make_url(contents, *args, **kwargs)
    html = '<iframe src={url} width={width} height={height}></iframe>'.format(
        url=url, width=width, height=height)
    return HTML(html)


def make_url(contents, domain=DEFAULT_DOMAIN, force_gist=False,
             size_for_gist=MAX_URL_LEN):
    """
    Returns the URL to open given the domain and contents.

    If the file contents are large, an anonymous gist will be created.

    Parameters
    ----------
    contents
        * string - assumed to be GeoJSON
        * an object that implements __geo_interface__
            A FeatureCollection will be constructed with one feature,
            the object.
        * a sequence of objects that each implement __geo_interface__
            A FeatureCollection will be constructed with the objects
            as the features
    domain - string, default http://geojson.io
    force_gist - force gist creation regardless of file size.

    For more information about __geo_interface__ see:
    https://gist.github.com/sgillies/2217756

    If the contents are large, then a gist will be created.

    """
    contents = make_geojson(contents)
    if len(contents) <= size_for_gist and not force_gist:
        url = data_url(contents, domain)
    else:
        gist = _make_gist(contents)
        url = gist_url(gist.id, domain)

    return url


def make_geojson(contents):
    """
    Return a GeoJSON string from a variety of inputs.
    See the documentation for make_url for the possible contents
    input.

    Returns
    -------
    GeoJSON string

    """
    if isinstance(contents, six.string_types):
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
                raise ValueError('Unknown type at index {0}'.format(i))
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


def data_url(contents, domain=DEFAULT_DOMAIN):
    """
    Return the URL for embedding the GeoJSON data in the URL hash

    Parameters
    ----------
    contents - string of GeoJSON
    domain - string, default http://geojson.io

    """
    url = (domain + '#data=data:application/json,' +
           urllib.parse.quote(contents))
    return url


def _make_gist(contents, description='', filename='data.geojson'):
    """
    Create and return an anonymous gist with a single file and specified
    contents

    """
    ghapi = github3.GitHub()
    files = {filename: {'content': contents}}
    gist = ghapi.create_gist(description, files)

    return gist


def gist_url(gist_id, domain=DEFAULT_DOMAIN):
    """
    Return the URL for loading GeoJSON data from a gist

    Parameters
    ----------
    contents - string, gist id
    domain - string, default http://geojson.io

    """
    url = (domain + '#id=gist:/{0}'.format(gist_id))
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
                        default=DEFAULT_DOMAIN,
                        help='Alternate URL instead of http://geojson.io/')

    parser.add_argument('filename',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="The file to send to geojson.io")

    args = parser.parse_args()

    contents = args.filename.read()
    url = make_url(contents, args.domain)
    if args.do_print:
        print(url)
    else:
        webbrowser.open(url)

if __name__ == '__main__':
    main()
