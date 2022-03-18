import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, jsonify

cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

#RETRIEVE INVENTORY
@app.route("/inventory/<userEmail>")
def getInventory(userEmail):
    try:
        userInventory = (
            db.collection("inventory").document(userEmail).get().to_dict()
        )
    except:
        return {"code": 401, "message": "Error occured retrieving inventory"}

    return {"code": 201, "data": userInventory}

#CREATE INVENTORY FOR NEW USER
@app.route("/inventory/add/<userEmail>")
def addInventory(userEmail):
    data = {"gyoza": 3, "dog": 8}
    try:
        db.collection("inventory").document(userEmail).set(data)
    except:
        return {"code": 401, "message": "Error occured when creating inventory"}

    return {"code": 201, "message": "Inventory Created"}


#UPDATE EXISTING INVENTORY
@app.route("/inventory/update")
def updateInventory():
    userEmail = "matthias123@gmail.com"
    data = {
        "email": "matthias1234@gmail",
        "gyoza": {
            "counter": 6,
            "foodDesc": "Delcious Dog",
            "foodName": "Fried Gyozas",
            "image": "https://images.unsplash.com/photo-1609183590563-7710ba1f90a9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
            "oldPrice": "$6.00",
            "currentPrice": "$3.00",
        },
    }

    try:
        userInventory = db.collection("inventory").document(userEmail).set(data)

    except:
        return {"code": 401, "message": "Could not update inventory"}

    return {"code": 201, "message": "Inventory updated succesfully"}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
