from flask import Flask, jsonify, request
from database import Database


DEFAULT_PORT = 5000


class MyWebService:
    app = None
    db = None
    port = DEFAULT_PORT

    def __init__(self, port=DEFAULT_PORT):
        self.app = Flask(self.__class__.__name__)
        self.app.add_url_rule("/q", "q", self.perform_query)
        self.port = port
        self.db = Database()

    def run(self):
        self.app.run(port=self.port)  # Blocks until webserver is killed

    def perform_query(self, *args, **kwargs):
        args = request.args
        return jsonify(args)


if __name__ == '__main__':
    mws = MyWebService()
    mws.run()
