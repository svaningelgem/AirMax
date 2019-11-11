from flask import Flask, jsonify, request
from database import Database, Cursor
from collections import namedtuple

# DEBUG
import random


DEFAULT_PORT = 5000


class MyWebService:
    app = None
    port = DEFAULT_PORT
    GeoPoint = namedtuple("GeoPoint", ("lng", "lat"))
    allowed_parameters = {'pm25': 20, 'pm10': 40, 'bc': 1.33, 'co': 4.5, 'no2': 0.25, 'o3': 0.065, 'so2': 0.085}

    def __init__(self, port=DEFAULT_PORT):
        self.port = port

        self.app = Flask(self.__class__.__name__)
        self.app.static_folder = 'static'
        self.app.add_url_rule("/q", "q", self.perform_query)
        self.app.add_url_rule("/", "", self.send_index)

    def run(self):
        self.app.run(port=self.port)  # Blocks until webserver is killed

    def send_index(self):
        return self.app.send_static_file('maps.html')

    def _get_val(original_value, parameter):
        # return original_value  # if not debugging!
        # DEBUG
        v = MyWebService.allowed_parameters[parameter]
        return random.gauss(v, v * 1.5)  # when debugging

    def perform_query(self):
        args = request.args

        parameter = 'pm10'  # parameter will be used as part of an fstring in the query, but don't worry
                            # as we check it against a whitelist
        if 'parameter' in args:
            parameter = args['parameter']
            if parameter not in MyWebService.allowed_parameters:
                raise ValueError("Invalid parameter passed")

        retVal = dict()
        with Cursor(Database()) as c:
            for row in c.execute(
                f"""select longitude, latitude, avg(value) as val, "average" as type, date
                from air_quality
                where date > strftime('%s', datetime('now') - 3*60*60)
                and parameter = '{parameter}'
                group by 1, 2

                union

                select longitude, latitude, value as val, "last_data" as type, date
                from air_quality a1
                where date=(select max(date) from air_quality a2 where a1.longitude=a2.longitude and a1.latitude=a2.latitude and a1.parameter = a2.parameter)
                and parameter = '{parameter}'
                order by date asc"""
            ):  # date is necessary to be in the query because of the "order by" clause
                cur = MyWebService.GeoPoint(lng=row[0], lat=row[1])
                if row[3] == 'average' or cur not in retVal:
                    retVal[cur] = row[2]

#        return jsonify(list({'lng': k.lng, 'lat': k.lat, 'val': v} for k, v in retVal.items()))
        return jsonify(list({'lng': k.lng, 'lat': k.lat, 'val': MyWebService._get_val(v, parameter)} for k, v in retVal.items()))


if __name__ == '__main__':
    mws = MyWebService()
    mws.run()
