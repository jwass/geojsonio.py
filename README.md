geojsonio.py
============

Open GeoJSON data on [geojson.io](http://geojson.io).
This is a python port of [geojsonio-cli](https://github.com/mapbox/geojsonio-cli).

Send data to geojson.io and open a browser within python

    from geojsonio import display
  
    with open('map.geojson') as f:
        contents = f.read()
        
    display(contents)
    
To easily embed geojson.io in an iframe in a Jupyter/IPython notebook, use
the `embed()` method

    embed(contents)

It can also be used on the command line. Read or pipe a file

    geojsonio map.geojson
    geojsonio < run.geojson

Options:

    --print prints the url rather than opening it
    --domain="http://custominstancedomain.com/"
