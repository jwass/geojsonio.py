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


