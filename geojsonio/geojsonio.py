#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import sys
import urllib
import webbrowser

import github3

MAX_URL_LEN = 150e3  # Size threshold above which a gist is created

def display(contents, domain='http://geojson.io/'):
    url = geojsonio_url(contents, domain)
    webbrowser.open(url)
    return url
# display() used to be called to_geojsonio. Keep it around for now...
to_geojsonio = display

def geojsonio_url(contents, domain='http://geojson.io/'):
    """
    Returns the URL to open given the domain and contents

    If the contents are large, then a gist will be created.

    """
    if len(contents) <= MAX_URL_LEN:
        url = _data_url(domain, contents)
    else:
        gist = _create_gist(contents)
        url = _gist_url(domain, gist.id)

    return url

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

