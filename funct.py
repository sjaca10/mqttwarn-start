import json
import time

def addInformation(topic, data, srv):
    payload = json.JSONDecoder().decode(data["payload"])

    # Insert into the data's payload (table's name) the outer information
    for i in payload:
        if i != "data":
            for j in payload["data"]:
                payload["data"][j][i] = payload[i]

    # Inserte into the data's payload (table's name) new information
    for x in payload["data"]:
        payload["data"][x]["modified"] = time.strftime('%Y-%m-%d %H:%M:%S')

    # Assign the new payload to the data's payload
    data["payload"] = payload

    return data