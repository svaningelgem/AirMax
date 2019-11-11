from sqs_listener import SqsListener
import os
import tempfile
import json
from config import Config
from database import Database
import dateutil.parser


def get_value(msg, search, default=NotImplemented):
    if not isinstance(msg, dict) or 'MessageAttributes' not in msg:
        if default is NotImplemented:
            raise ValueError("Invalid message")
        else:
            return default

    tmp = msg['MessageAttributes']
    if not isinstance(tmp, dict) or search not in tmp:
        if default is NotImplemented:
            raise ValueError(f"Couldn't find {search} in the message")
        else:
            return default

    tmp = tmp[search]
    if not isinstance(tmp, dict) or 'Value' not in tmp:
        if default is NotImplemented:
            raise ValueError("Invalid entry found in the message")
        else:
            return default

    return tmp['Value']


class MyListener(SqsListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        os.makedirs(Config.cache_dir, mode=0o755, exist_ok=True)
        self.db = Database()

    def handle_message(self, body, attributes, messages_attributes):
        # Save for debugging purposes
        with tempfile.NamedTemporaryFile(dir=Config.cache_dir, delete=False, mode="w") as tmp:
            json.dump(obj=body, fp=tmp)

        # We only want Belgian ones here! (ok it's preselected, but I still like to make certain)
        if get_value(body, 'country') != 'BE':
            return

        self.db.add_measurement(
            date=dateutil.parser.parse(get_value(body, 'date_utc')).timestamp(),
            latitude=get_value(body, 'latitude'),
            longitude=get_value(body, 'longitude'),
            country=get_value(body, 'country', ''),
            city=get_value(body, 'city', ''),
            location=get_value(body, 'location', ''),
            value=get_value(body, 'value'),
            unit=get_value(body, 'unit', 'µg/m³'),
            parameter=get_value(body, 'parameter', ''),
            sourceType=get_value(body, 'sourceType', ''),
            sourceName=get_value(body, 'sourceName', ''),
        )


if __name__ == "__main__":
    listener = MyListener('openaq_steven', region_name='eu-west-1')
    listener.listen()
