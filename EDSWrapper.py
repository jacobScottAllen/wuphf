import json
from datetime import datetime

class eds_wrapper:
    def __init__(self):
        self.omf_type = [{
            "id": "wuphf",
            "type": "object",
            "classification": "dynamic",
            "properties":{
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
        }]

        self.omf_container = [{
            "id": "dining room",
            "typeid": "wuphf"
        }]

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

        write_json_to_file(omf_value)
    


def write_json_to_file(json_string):
    with open("data_file.json", "w") as write_file:
        json.dump(json_string, write_file)