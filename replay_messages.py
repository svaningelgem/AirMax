from database import Database
import glob
import json
import dateutil
from listener import MyListener


db = Database()
for f in glob.glob('cache/tmp*'):
    with open(f, "r") as fp:
        body = json.load(fp)

        country = MyListener._get_value(body, 'country', '')
        db.add_measurement(
            date=dateutil.parser.parse(MyListener._get_value(body, 'date_utc')).timestamp(),
            latitude=MyListener._get_value(body, 'latitude'),
            longitude=MyListener._get_value(body, 'longitude'),
            country=country,
            city=MyListener._get_value(body, 'city', ''),
            location=MyListener._get_value(body, 'location', ''),
            value=MyListener._get_value(body, 'value'),
            unit=MyListener._get_value(body, 'unit', 'µg/m³'),
            parameter=MyListener._get_value(body, 'parameter', ''),
            sourceType=MyListener._get_value(body, 'sourceType', ''),
            sourceName=MyListener._get_value(body, 'sourceName', ''),
        )
