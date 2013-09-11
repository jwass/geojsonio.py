import webbrowser
import urllib

import github3

MAX_URL_LEN = 150e3  # Size threshold above which a gist is created

def to_geojsonio(contents, domain='http://geojson.io/'):
    url = geojsonio_url(contents, domain)
    webbrowser.open(url)


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


