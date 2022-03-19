import requests
from flask import Flask, request, jsonify
import json

# userLocation = '556 Choa Chu Kang North 6'
# storeAddress = 'Changi Prison'

APIKEY = "AIzaSyCd5JgqK3vcSWsx29XrLb7e4BnMjI2rtBw"

app = Flask(__name__)

@app.route("/stores/getDistance/<storeEmail>")
def getDistance():
    #{
    #   "userLocation": Take from browser, 
    #   "storeLocation": Take from frontend
    # }
    locations = request.get_json()
    userLocation = locations["userLocation"]
    storeAddress = locations["address"]

    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        + "?origins={}".format(userLocation)
        + "&destinations={}".format(storeAddress)
        + "&key={}".format(APIKEY)
    )

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    answer = json.loads(response.text)
    distance = answer["rows"][0]["elements"][0]["distance"]["text"]

    return "Distance to travel: {}".format(distance)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
