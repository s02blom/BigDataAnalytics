import threading
import time
from . import db
import pandas as pd

class Timer(threading.Thread):

    def __init__(self):
        self._timer_runs = threading.Event()
        self._timer_runs.set()
        super().__init__()

    def run(self):
        while self._timer_runs.is_set():
            self.timer()
            time.sleep(self.interval)

    def timer():
        return NotImplementedError

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
        self.interval = int(interval)
        self.data = {"count": [], "time": [], "iso_time": []}
        self.self_stop = 0
        super().__init__()

    def timer(self) -> None:
        """
        The function that is run once every interval. 
        Currently we only get the count for the collection and take the current time and save that in data
        """
        if not (self.self_stop % 100):
            if (self.check_if_self_stop(5)):
                self.stop()
        collection = self.database[self.collection_name]
        count = collection.count_documents({})
        if self.self_stop > 0 or count != 0:
            timestamp = time.localtime()
            self.data["count"].append(int(count))
            self.data["time"].append(timestamp)
            self.data["iso_time"].append(time.strftime('%H:%M:%S', timestamp))
            self.self_stop += 1

    def check_if_self_stop(self, min_similarity_length: int) -> bool:
        """
        The function check if the last 5 recorded datapoints have the same count
        
        Parameters:
        min_similarity_length (int): the number of items looked at to see if they are the same
        """
        return len(self.data["count"]) >= min_similarity_length and len(set(self.data["count"])) == 1

    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.data, columns=["count", "time"])

    def stop(self):
        """Stops the timer and closes the database connection. """
        # db.close_connection(self.database)
        super().stop()