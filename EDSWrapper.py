import json
from datetime import datetime
import requests

class eds_wrapper:
    def __init__(self):
        self.digest_config_file()

        self.set_up_type()
        self.set_up_container()
        self.insert_value(21)

    def insert_value(self, value, containerid = "dining room", timestamp = None):
        if timestamp is None:
            timestamp = datetime.now()

        omf_value = [{
            "containerid": containerid,
            "values":[{
                "timestamp":str(timestamp),
                "sound level":str(value)
            }]
        }]

        header = self.get_omf_header_json("data", "create")
        body = omf_value

        self.send_omf_post(header, body, "data")


    def digest_config_file(self):
        config_file = "config.json"
        
        with open(config_file, "r") as read_file:
            self.config = json.load(read_file)

        print("Using " + self.config["endpoint"] + " as the endoint")

    def set_up_type(self):
        header = self.get_omf_header_json("type", "create")
        
        type_properties = {
            "timestamp":{
                "type":"string",
                "format": "date-time",
                "isindex":True
            },
            "sound level":{
                "type":"number",
                "format":"float64"
            }
        }

        omf_type = self.get_omf_type_json("wuphf", "dynamic", type_properties)

        self.send_omf_post(header,omf_type, "create")
    
    def set_up_container(self):
        header = self.get_omf_header_json("container", "create")
        
        body = self.get_omf_container_json("wuphf", "dining room")

        self.send_omf_post(header, body, "create")

    def get_omf_container_json(self, typeid, containerid):
        omf_container = [{
            "id": containerid,
            "typeid": typeid
        }]

        return omf_container

    def get_omf_header_json(self, messagetype, action):
        # Defaults that may get exposed to parameters later
        messageformat = "JSON"
        omfversion = "1.0"
        compression = "none"

        header = {
            "producertoken": self.config["producer token"],
            "messagetype":messagetype,
            "action":action,
            "messageformat":messageformat,
            "omfversion":omfversion,
            "compression":compression
        }

        return header

    def get_omf_type_json(self, id, classification, properties):
        type_body = [{
            "id":id,
            "type": "object",
            "classification": classification,
            "properties":properties
        }]

        return type_body

    def send_omf_post(self, headers, body, message_type):
        timout_in_seconds = 10

        response = requests.post(
            self.config["endpoint"],
            headers = headers,
            json = body,
            verify = False,
            timeout = timout_in_seconds
        )

        print("Response code: " + str(response.status_code))

    


def write_json_to_file(json_string):
    with open("data_file.json", "w") as write_file:
        json.dump(json_string, write_file)