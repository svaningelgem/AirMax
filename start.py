import threading
from listener import MyListener
from webservice import MyWebService


class SqsListener(threading.Thread):
    def run(self):
        listener = MyListener('openaq_steven', region_name='eu-west-1')
        listener.listen()


if __name__ == "__main__":
    threads = list()

    try:
        # Start all our logic in separate threads
        threads.append(SqsListener().start())  # Ingest SQS data --> Store in SQLite
        threads.append(MyWebService())         # Start flask service to provide AJAX support

        for t in threads:
            t.join()
    except Exception as e:
        print(e)
