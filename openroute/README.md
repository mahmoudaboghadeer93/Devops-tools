# OpenRoute 

https://github.com/GIScience/openrouteservice
Geospatial data for quite a while similar to google maps that it provides like geocoding, route-directions, etc. 

## prerequisite

OSM extract from Geofabrik

For Egypt  
PBF=http://download.geofabrik.de/africa/egypt-latest.osm.pbf

For UAE, KSA, Kuwait, Bahrain and Oman 
http://download.geofabrik.de/asia/gcc-states-latest.osm.pbf


For Pakistan 
http://download.geofabrik.de/asia/pakistan-latest.osm.pbf


## Docker Build
You should pass the COUNTRY and CONTINENT Args `--build-arg=COUNTRY=gcc-states` `--build-arg=CONTINENT=asia` . 
E.g
`docker build -t openroutes-gcc --build-arg=COUNTRY=gcc-states --build-arg=CONTINENT=asia`
