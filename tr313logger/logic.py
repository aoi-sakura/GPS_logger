# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import and_

from tr313logger import DATE_FORMAT
from tr313logger.model import Location
from tr313logger.repository.utility import session_scope


def get_latest_point():
    with session_scope() as session:
        result = session.query(Location).order_by(Location.seq_no.desc()).first()
        return __locations_to_geojson_point([result])


def get_latest_points(start: datetime, end: datetime):
    with session_scope() as session:
        result = session.query(Location).filter(and_(Location.datetime >= start, Location.datetime <= end)).all()
        return __locations_to_geojson_point(result)


def register_location(location: Location):
    with session_scope() as session:
        session.add(location)


def __locations_to_geojson_point(locations):
    features = []
    for location in locations:
        geometry = {'type': 'Point',
                    'coordinates': [location.longitude, location.latitude]}
        properties = {'num_of_satellites': location.num_of_satellites,
                      'datetime': location.datetime.strftime(DATE_FORMAT),
                      'report_type': location.report_type,
                      'status': location.status}
        features.append({'type': 'Feature', 'geometry': geometry, 'properties': properties})

    geojson = {'features': features, 'type': 'FeatureCollection'}

    return geojson
