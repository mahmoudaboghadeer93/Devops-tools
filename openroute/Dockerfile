FROM openrouteservice/openrouteservice:latest


ARG COUNTRY
ARG CONTINENT

ENV COUNTRY=$COUNTRY
ENV CONTINENT=$CONTINENT
ENV PROFILE=$PROFILE

RUN [ ! -z $COUNTRY ] && [ ! -z $CONTINENT ] 

RUN wget https://download.geofabrik.de/${CONTINENT}/${COUNTRY}-latest.osm.pbf

RUN mv ${COUNTRY}-latest.osm.pbf ./ors-core/data/osm_file.pbf
