import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, jsonify

cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)


# {  
#     "email": "matthiasnew3@gmail.com",
#     "first_name": "mathias",
#     "last_name": "Lee",
#     "phone_number": 91774280,
#     "image": "xx",
#     "shop_name": "Koufuck",
#      ""
# }


# GET ALL SELLERS
@app.route('/sellers')
def getSellers():
    result = []
    allSellers = db.collection('sellers').get()
    for seller in allSellers:
        seller = seller.to_dict()
        result.append(seller)
    
    if len(result) == 0:
        return {'code': 401, 'message': 'NO SELLERS IN DB'}

    return {"code": 200, "data": {"stores": result}}

#ADD SELLER
@app.route('/sellers/add/', methods=['POST', "GET"])
def addSeller():
    sellerData = request.get_json()
    allSellers = db.collection('sellers').get()

    for seller in allSellers:
        seller = seller.to_dict()
        if seller['email'] == sellerData['email']:
            return jsonify({'code': 404, 'message': 'Seller already exists'})
    
    try:
        db.collection('sellers').document(sellerData['email']).set(sellerData)
        print('Added Seller')

    except: 
        return jsonify({"code": 404, "message": "Error occured when adding store"})

    return jsonify({"code": 201, "message": "Successfully Added Seller"})
    

#UPDATE SELLER INFO
@app.route('/sellers/update/<userEmail>', methods=['POST', 'GET'])
def updateSeller(userEmail):
    sellerRef = db.collection('sellers').document(userEmail)
    sellerInfo = request.get_json()
    
    #EMAIL CHANGE
    if userEmail != sellerInfo['email']:
        try:
            #CREATE NEW
            db.collection('sellers').document(sellerInfo['email']).set(sellerInfo)

            #DELETE OLD
            db.collection('sellers').document(userEmail).delete()
        except:
            return jsonify({"code": 404, "message": "Error occured when adding store"})

        return jsonify({"code": 201, "message": "Successfully Updated Email Address and Information"})
    
    #ANY OTHER CHANGE
    else:
        try:
            sellerRef.update(sellerInfo)

        except:
            return jsonify({"code": 404, "message": "Error occured when adding store"})
            
        return jsonify({"code": 201, "message": "Successfully Updated Information"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
