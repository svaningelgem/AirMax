import threading
from listener import MyListener
from webservice import MyWebService
import webbrowser


class SqsListener(threading.Thread):
    def run(self):
        listener = MyListener('openaq_steven', region_name='eu-west-1')
        listener.listen()


class Webserver(threading.Thread):
    def run(self):
        web = MyWebService()
        web.run()


if __name__ == "__main__":
    threads = list()

    try:
        # Start all our logic in separate threads
        threads.append(SqsListener())  # Ingest SQS data --> Store in SQLite
        threads.append(Webserver())         # Start flask service to provide AJAX support

        for t in threads:
            t.start()

        webbrowser.open("http://127.0.0.1:5000/")

        for t in threads:
            t.join()
    except Exception as e:
        print(e)
