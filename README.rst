============
geojsonio.py
============

Open GeoJSON data on `geojson.io <http://geojson.io>`_ from Python.
``geojsonio.py`` also contains a command line utility that is a Python port of `geojsonio-cli
<https://github.com/mapbox/geojsonio-cli>`_.

.. image:: https://travis-ci.org/jwass/geojsonio.py.svg?branch=master
    :target: https://travis-ci.org/jwass/geojsonio.py

Usage
-----

Send data to geojson.io and open a browser within python

.. code-block:: python

    from geojsonio import display
    
    with open('map.geojson') as f:
        contents = f.read()
        display(contents)
        
Data
----
There are two methods by which ``geojsonio.py`` gets geojson.io to render the data:

- Embedding the GeoJSON contents in the geojson.io URL directly
- Creating an anonymous Github gist and embedding the gist id in the geojson.io URL.

``geojsonio.py`` automatically determines which method is used based on the length of the GeoJSON contents.
If the contents are small enough, they will be embedded in the URL. Otherwise ``geojsonio.py`` creates an anonymous
Gist on Github with the GeoJSON contents. Note: when an anonymous gist is created, the data is uploaded to Github
and a unique gist ID is created. If anyone else is able to obtain the gist ID, they will be able to see your data.
    
Goes Great With GeoPandas
-------------------------
``geojsonio.py`` integrates nicely with `GeoPandas <https://github.com/geopandas/geopandas>`_ to
display data in a ``GeoDataFrame``.

Say you have a file containing the borders of all states called ``states.geojson``. Each GeoJSON record has a
property called ``'Name'``. Quickly display all the states whose names start with ``'M'``

.. code-block:: python

    import geopandas as gpd
    import geojsonio
    
    states = gpd.read_file('states.geojson')
    m_states = states[states['Name'].str.startswith('M')]
    geojsonio.display(m_states.to_json())

This will open a browser to the geojson.io window with the polygons drawn on the slippy map.

IPython Notebook Integration
----------------------------
    
To easily embed geojson.io in an iframe in a Jupyter/IPython notebook, use
the ``embed()`` method

.. code-block:: python

    embed(contents)

Command Line Interface
----------------------

It can also be used on the command line. Read or pipe a file

::

    $ geojsonio map.geojson
    $ geojsonio < run.geojson

Options:

::

    --print prints the url rather than opening it
    --domain="http://custominstancedomain.com/"

Installation
------------
Install with ``pip``

::

    $ pip install geojsonio


