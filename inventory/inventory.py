import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, jsonify

cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
app = Flask(__name__)

# RETRIEVE INVENTORY
@app.route("/inventory/<userEmail>")
def getInventory(userEmail):
    try:
        userInventory = db.collection("inventory").document(userEmail).get().to_dict()
    except:
        return {"code": 401, "message": "Error occured retrieving inventory"}

    return {"code": 201, "data": userInventory}


# CREATE INVENTORY FOR NEW USER
@app.route("/inventory/add/<userEmail>")
def addInventory(userEmail):
    data = request.get_json()
    try:
        db.collection("inventory").document(userEmail).set(data)
    except:
        return {"code": 400, "message": "Error occured when creating inventory"}

    return {"code": 200, "message": "Inventory Created"}


# UPDATE / ADD EXISTING INVENTORY
@app.route("/inventory/update/<userEmail>", methods=["POST", "GET"])
def updateInventory(userEmail):
    # newFoods = request.get_json()
    newFoods = {
        "gyoza": {
            "item_quantity": 6,
            "food_desc": "Yummy Gyoza",
            "food_name": "Fried Gyozas",
            "image": "https://images.unsplash.com/photo-1609183590563-7710ba1f90a9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
            "old_price": "$6.00",
            "current_price": "$3.00",
        },
        "dog": {
            "item_quantity": 10,
            "food_desc": "Delicious Dog",
            "food_name": "Fried dog",
            "image": "https://images.unsplash.com/photo-1618173745201-8e3bf8978acc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=930&q=80",
            "old_price": "$10.00",
            "current_price": "$5.00",
        },
        "cat": {
            "item_quantity": 10,
            "food_desc": "Delicious cat",
            "food_name": "Fried cat",
            "image": "https://images.unsplash.com/photo-1618173745201-8e3bf8978acc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=930&q=80",
            "old_price": "$10.00",
            "current_price": "$10.00",
        },
    }

    successUpdate = ""
    successAdd = ""
    message = ""

    userInventory = db.collection("inventory").document(userEmail).get().to_dict()
    invSnap = db.collection("inventory").document(userEmail)

    for food_name, foodDetails in newFoods.items():
        # UPDATE DISH
        if food_name in userInventory.keys():
            try:
                invSnap.update({food_name: foodDetails})
                successUpdate += food_name + ", "
            except:
                return {
                    "code": 400,
                    "message": "Failed to Update {} details".format(food_name),
                }
        # NEW DISH
        else:
            try:
                invSnap.update({food_name: foodDetails})
                successAdd += food_name + ", "
            except:
                return {
                    "code": 400,
                    "message": "Failed to Add {} details".format(food_name),
                }

    if successUpdate and successAdd:
        message += (
            "Sucessfully updated details of {}. Succesfully added details of {}".format(
                successUpdate[:-2], successAdd[:-2]
            )
        )
    elif successUpdate:
        message += "Sucessfully updated details of {}".format(successUpdate[:-2])
    else:
        message += "Succesfully added details of {}".format(successAdd[:-2])

    return {"code": 201, "message": message}


# DELETE FOOD
@app.route("/inventory/delete/<userEmail>", methods=["DELETE"])
def deleteInventory(userEmail):
    # target = request.get_json(())

    target = {
        "gyoza": {
            "item_quantity": 6,
            "food_desc": "Yummy Gyoza",
            "food_name": "Fried Gyozas",
            "image": "https://images.unsplash.com/photo-1609183590563-7710ba1f90a9?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
            "old_price": "$6.00",
            "current_price": "$3.00",
        }
    }

    userInventory = db.collection("inventory").document(userEmail).get().to_dict()
    dbSnap = db.collection("inventory").document(userEmail)
    targetItem = list(target.keys())[0]

    if targetItem in userInventory:
        try:
            dbSnap.update({targetItem: firestore.DELETE_FIELD})

        except:
            return {"code": 400, "message": "Failed to delete {}".format(targetItem)}

    else:
        return {"code": 200, "message": "SPAM, DELETED"}

    return {"code": 200, "message": "{} Successfully Deleted".format(targetItem)}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
