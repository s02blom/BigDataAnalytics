import threading
import time
from . import db


class Timer(threading.Thread):

    def __init__(self):
        self._timer_runs = threading.Event()
        self._timer_runs.set()
        super().__init__()

    def run(self):
        while self._timer_runs.is_set():
            self.timer()
            time.sleep(self.__class__.interval)

    def stop(self):
        self._timer_runs.clear()

class CollectionTimer(Timer):
    """
    A timer class that will collect data about a Mongo collection. 
    The data is the current document count of the collection along with the 
    time when the data was gathered. This is stored in the data variable

    Methods:
    __init__(collection_name, database, interval)
    stop

    Variables:
    data (list[list[int, time.struct_time]]): A list keeping track of the aquired data
    """
    def __init__(self, collection_name: str, database, interval = 10):
        """
        Parameters:
        collection_name (string): The name of the collection to be accessed by this timer
        database (pymongo.synchronous.database.Database): A connection to the database, preferably gotten from the db.py file
        interval (int): The number of seconds the timer will sleep inbetween iterateions. Defaults to 10 seconds
        """
        self.collection_name = collection_name
        self.database = database
        self.interval = interval
        self.data = []
        super().__init__()

    def timer(self) -> None:
        """
        The function that is run once every interval. 
        Currently we only get the count for the collection and take the current time and save that in data
        """
        count = self.database[self.collection_name].count_documents({})
        timestamp = time.localtime()
        data_entry = [count, timestamp]
        self.data.append(data_entry)

    def stop(self):
        """Stops the timer and closes the database connection. """
        db.close_connection(self.database)
        super().stop()