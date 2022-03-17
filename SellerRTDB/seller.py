from flask import Flask, request, jsonify
import pyrebase
import json

config = {
    "apiKey": "apiKey",
    "authDomain": "projectId.firebaseapp.com",
    "databaseURL": "https://nomnom-db-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "projectId.appspot.com",
}

app = Flask(__name__)

# Database initilisation
firebase = pyrebase.initialize_app(config)
db = firebase.database()


# GET ALL STORES IN DB
@app.route("/stores")
def get_all():
    storesArray = []
    allStores = db.child("storeCollection").get()
    if allStores:
        for store in allStores.each():
            storesArray.append(store.val())

        return jsonify({"code": 200, "data": {"stores": storesArray}})

    return jsonify({"code": 404, "message": "i need cigg -EKLum"})


# SEARCH FOR STORE
@app.route("/stores/<string:inputStoreName>", methods=["POST", "GET"])
def get_store(inputStoreName):
    allStores = db.child("storeCollection").get()
    for store in allStores.each():
        indivStore = store.val()
        storeName = indivStore["details"]["storeName"].replace(" ", "").lower()

        if storeName == inputStoreName.lower():
            return jsonify({"code": 200, "data": {"store": indivStore}})

    return jsonify({"code": 404, "message": "Store no have sir"})


# ADD STORE
@app.route("/stores/add/<string:inputStoreName>", methods=["POST", "GET"])
def add_store(inputStoreName):
    allStores = db.child("storeCollection").get()
    for store in allStores.each():
        indivStore = store.val()
        storeName = indivStore["details"]["storeName"].replace(" ", "").lower()

        if storeName == inputStoreName.lower():
            return jsonify({"code": 404, "message": "Store already exists"})

    print("CREATION START")
    storeData = request.get_json()
    try:
        db.child("storeCollection2").push(storeData)
        # if storeData == null:
        #     print ('Nothing to add')
        print('Added to Database')

    except:
        return jsonify({"code": 404, "message": "Error occured when adding store"})

    return jsonify({"code": 201, "message": "Successfully Added Store"})


# UPDATE STORE
# Authenticate first?
@app.route("/stores/update/<string:userStore>")
def update_store(userStore):
    pass


if __name__ == "__main__":
    app.run(port=5000, debug=True)
