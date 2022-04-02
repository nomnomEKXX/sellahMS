import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, jsonify

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "nomnom-db",
        "private_key_id": "d8d4891c11e74bf544eeadf17e6a5605d9577382",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCo+kUgAqCNm1j+\nc000e87vSjyi1Y5WfLx8v1ma8KrBbeJ3aNbV9iTeNqqIWAnr/qsC8ctxiO8FSBKp\naycpjRjWDpCVkE7V5FxUxOmyu9bB84FVS1Udr+u9d2/9gaZ2oia3xqzBYrh5fquM\n+fDUIdnB1Zy7A267xUGdLn4gw1xweELTDB7O58idF71sb1ipBVvy1EfWN1htJejU\nzMujQJK+gfijjYVujPYkNUp1cjQUGICVZj1JHEGVX5cvuMqtr9ij7biM1NPPpv3D\nMOhzKQLhgK/Ajo3T4uZfy5uOGzxPMQWuX6VGCcFSszvyALx6HHY5IDgU5bqQ1edd\nlf4qifedAgMBAAECggEALKbluU24a3MPkz2YuzO0PRta5pSUJlqT3EscPIs4NCD7\nZR55FtUSbP35FkpdZNVJD2AhqIDM2JJxC//au2ojk/0JS9x0WKUdmPDn6GkmmN3l\n4Uok1dF08/4pw82M1XCH1qxTXk7d/IzyfDBX6VaAmm3+GpUPn+LCMezlO3ckaDuQ\n6CgWLbp8u9gGMqQkxG3oqYUjtgeFjRXkw8ILIhn0pEPGBItMyQexK6pbPGeltkq5\nOcxvNtTm4SsqYgdx79Do2FUvFuwhHcz2Fugk6gg0dB8JHHamNlrG9SOsFw9Uwm2r\nYY1C4B6z1r0T8mY8mazID3qvsDxk/h93cYPlpWdIKQKBgQDivg3XdhJtXqTd8T9J\n6qcMafbB9xbAVrfjqnpd+9CVHtany6tyd9KlDhJEPINZhjoYynr/5mOKFz6SZdlG\n+u21s8l4Pu54lrDIG2z4mULMfAkNa7Be9thLLJ3Qefahfswyoqe26aeNbtQRZlqX\niw6mFp4dT7BZIhIEinUE33l8lwKBgQC+yBS+K4BDO4pJm7u6xYroVT+Zog7kHmug\nrisQjY1lgrCS+YIWcpEhWV+tdUp5BXsTUZ7M36FdcBXKcJ69Jzr8oi3l1cLCjUdl\nSS9J5wJo8nBfYARt/6WfqlgzSHsdDLqYGv5vtxgVtoGN8xA1E8/ZeS4999n6bAJG\nFpNQBD5P6wKBgCe+BjEQyfQPlbgtE9nB3lvHqu+efodh68Nk2yPkAlBQ4nDwuvFK\nXUp+5+a78I3dgAteWibGXAYVQutoHKhbTRT/GT4RUb0jNIMug3AjdNjgmLmYeYZ7\nn7e1b0feSMNPtTze06S02aBpn5QZK6HKRtwHtNkQYamN1jijiBU9kk6rAoGBAKAz\ncvedn77VKHJXC3TynIory5Q+uTJlOQtcNV1Y//rVm2BPlCU1XxkZ63XEoByvtYGr\ncCWpQ98qV6H+n81GPAoYRWJR9ZFZATLUGZl9GlD2A9aS0iVsHq/MYvPtUTQ7lBRV\n1oIIxXi2IGQKTvnDAS4ky+fNUIUwXVhtbJYsegaxAoGANUKGJmOMOSIbDjwgexva\n+bjVnQGUthCV/x/UqeFMdOKM2doPu78uQWXG9u7nxN63b3FWlCuKHnjq7nA5zEhz\nNWf50KWtQ2BIaGvAQJhw+ti9CuVi18WOM0nXfRjI/+0YsLcWQIZjKAIcvc83cwjX\nSOvsvytCXrSg65ayi7xb9t0=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-bhktu@nomnom-db.iam.gserviceaccount.com",
        "client_id": "108783214540036148659",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-bhktu%40nomnom-db.iam.gserviceaccount.com",
    }
)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)


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
@app.route('/sellers/update/<userEmail>', methods=['POST', 'GET', "PUT"])
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
    app.run(host='0.0.0.0', port=5000, debug=True)

