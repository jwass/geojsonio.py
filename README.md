geojsonio.py
============

Open GeoJSON data on geojson.io.
A python port of [geojsonio-cli](https://github.com/mapbox/geojsonio-cli).

Read or pipe a file

    geojsonio map.geojson
    geojsonio < run.geojson

Options:

    --print prints the url rather than opening it
    --domain="http://custominstancedomain.com/"
    

You can also send data and open a browser within python

    from geojsonio import to_geojsonio
  
    with open('map.geojson') as f:
        contents = f.read()
        
    to_geojsonio(contents)

For larger files, an anonymous gist will be created and used by geojson.io. That feature may change soon.
