from datetime import datetime, timedelta
import json
import requests

class EDSEgress:
    """A class for retreiving data from EDS's egress endpoint"""
    def __init__(self):
        self.config = self._get_config_file()
        self.session = self._setup_session()

    def lastValue(self):
        """The most recent value in EDS
        
        Returns:
            json -- The single entry from EDS as a dict[Timestamp, Volume]
        """
        print(self.config["egress"] + "GetLastValue")
        response = self.session.get(url=self.config["egress"] + "GetLastValue")
        return response.json()

    def window_of_values(self, start_time: datetime, end_time: datetime = datetime.utcnow()):
        """Retrieves the values within EDS for the given time range
        
        Arguments:
            start_time {datetime} -- The start time for the window
        
        Keyword Arguments:
            end_time {datetime} -- The end time for the window (default: {datetime.utcnow()})
        
        Returns:
            json -- Multiple entries from EDS as a list of dict[Timestamp, Volume]
        """
        params = { "startIndex": start_time.isoformat(), "endIndex": end_time.isoformat() }
        response = self.session.get(url=self.config["egress"] + "GetWindowValues", params=params)
        return response.json()

    def _get_config_file(self):
        config_file = "config.json"
        
        with open(config_file, "r") as read_file:
            config = json.load(read_file)

        print("Using " + config["egress"] + " as the endoint")
        print("This pi is in " + config["location"])
        return config

    def _setup_session(self):
        session = requests.Session()
        session.verify = False
        session.headers = {"producertoken": self.config["producer token"]}
        return session

def main():
    eds_egress = EDSEgress()
    print("\nLast Values is: " )
    print(eds_egress.lastValue())
    yesterday = datetime.utcnow() - timedelta(days=1)
    print("\nLast day of values is: ")
    print(eds_egress.window_of_values(yesterday))

if __name__ == '__main__':
    # disable https warnings
    requests.packages.urllib3.disable_warnings()
    main()