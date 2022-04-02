import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, jsonify

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "nomnomsellers",
        "private_key_id": "dd4607d02b9221005ec71fc32f24bf8e62a9bea6",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCpeh3Y2rkWjcMh\nQ5JNEQj2t4zmMobzwudxZQN/HMT+WgG9nkeEkAa6PDUFMfcBwleVMx/EECOISPeq\ntu0pYNrPTXHUYdvZRcPIqGlCDAoKDV3aK4zrGEo8ByQ1YLjUG7P+UWzR/CGdgPG0\nVIJrWrfnXtEc/3qnE6BcVyycwgPQ9mpIO5ZbfKje6YwZOuLL/uXgMjnluflfjZQK\nPsYkAEoCj4amQt7LuOFAjJWE5S5Rt0i1VnOoUEckAJ0C5i7i5z9iezX+WXXeAWkv\nV3hr8v5wEVHKHWn2zBE4Ua7EHaW1EHIBlfQpDVTdRsfBH8Zod9GCBPXY0hlpQbPS\n7HnugHFhAgMBAAECggEATDEd7Qm8L2MRSEmgIuyXKo/vlOg/WqSTt5uRvFpbR/yA\nDtbzUSoNFDoQHiNN6KkOBgIjdFpLFzCyw7mUmscz6AHpvHE4TRB7yiDInYxbERTc\nTkLJCkJz0VPml+bBgX5o59uEgE0Jcc1wHMHnlksFJcwvWAmVgzqkHA+G+3yQCaea\nwj83NBNqggtq3iMcTtBgj4sBMrLgkS1OO3FsyFhtuzSA4RmPr66yuRSZtlkFzYu4\nJ3lnNR9jAJxnzwT9AypM7xIbkFLalvtR3pjLDLmqfA8BGd6FODHGwtywL20Pw4VG\nDh4UkaZMkrfFNXtlAyxvfd/JVKTaKWM/wwjgthgY/wKBgQDikVyqUBqxl3+PznkY\nQp6K3vXiJ+FiiRgx8Q+L42KtqdQjyol+8iHF+pVQz/Go9FD1ygqYJ1KFxVGR7TE4\nT7FeOgFdeNV+SpXRCJaBDKUW4hjWgCfVHr+cioFTmxLosWH8oKpHCQIWukqSbLlm\n6D4CHLKqx/4/qEFy3FbTbWHjPwKBgQC/fisfXb3yw/jEmMya0IN+ZiVZrWo/tyrP\nCQxU6m0VZYqcf5OSWL8MpLfHAxCrmDfAKj7dwQfVSwj3xldxIMgdNhc/2S4LjXpd\nz8zOyGR4vJpiwMj+l6pRLhTdwDBPoIelNf9Gwc6nhII6YmNIxUaHa4yBfy5saJ7B\nocgPaYSjXwKBgQDhYq+nMZbMciRQv5pRWvxys4gxGXEp3621CNRpWaNxlQ9XJ4WO\nRnr4guYFBUemxpy/VeUiJYP/VSJnI2kiVozgap2vCaSARNwynPNzn0ufrv38bHKz\nnSoKJPKwZAT0fHk4oe+iSMDOMTY74XKyf3goC7plEBzJ4KxzAeRR4W9OawKBgCw0\nmw3VnRjixpXT1D/U7NYMDIlEMCffR+GdbBxaNa5fz3zLMqzxEcGAcPBfM8T5Eb2p\nwvN8MSu686oHPn5eG/QqXXme0DNYiKwJYXVG63K3z0gGyx+CsY2l/qkmScDIBShN\na83Qxb0EKPADcHoHGH4AhOIMExJxoFyA1WdBa54vAoGAGSrX8WjUpk/bOirszoms\nbH4eZNWG2Bj/LPmjA1/YdTV1u8U2tdpPdLioBIm76YgauTb0L9EeD0a4cOyt8Lrl\n1oFfEeThFiVpchEurcH7pLHN/VmnWuRvjY5yu9HazfjmIqbjw70GKEhQa0aNFuXs\n0dCpz3OmyWdy9mYdZzYgH3I=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-km4tu@nomnomsellers.iam.gserviceaccount.com",
        "client_id": "104234272335999461863",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-km4tu%40nomnomsellers.iam.gserviceaccount.com",
    }
)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)


# GET ALL SELLERS
@app.route("/sellers")
def getSellers():
    result = []
    allSellers = db.collection("sellers").get()
    for seller in allSellers:
        seller = seller.to_dict()
        result.append(seller)

    if len(result) == 0:
        return {"code": 401, "message": "NO SELLERS IN DB"}

    return {"code": 200, "data": {"stores": result}}


# ADD SELLER
@app.route("/sellers/add/", methods=["POST", "GET"])
def addSeller():
    sellerData = request.get_json()
    allSellers = db.collection("sellers").get()

    for seller in allSellers:
        seller = seller.to_dict()
        if seller["email"] == sellerData["email"]:
            return jsonify({"code": 404, "message": "Seller already exists"})

    try:
        db.collection("sellers").document(sellerData["email"]).set(sellerData)
        print("Added Seller")

    except:
        return jsonify({"code": 404, "message": "Error occured when adding store"})

    return jsonify({"code": 201, "message": "Successfully Added Seller"})


# UPDATE SELLER INFO
@app.route("/sellers/update/<userEmail>", methods=["POST", "GET"])
def updateSeller(userEmail):
    sellerRef = db.collection("sellers").document(userEmail)
    sellerInfo = request.get_json()

    # EMAIL CHANGE
    if userEmail != sellerInfo["email"]:
        try:
            # CREATE NEW
            db.collection("sellers").document(sellerInfo["email"]).set(sellerInfo)

            # DELETE OLD
            db.collection("sellers").document(userEmail).delete()
        except:
            return jsonify({"code": 404, "message": "Error occured when adding store"})

        return jsonify(
            {
                "code": 201,
                "message": "Successfully Updated Email Address and Information",
            }
        )

    # ANY OTHER CHANGE
    else:
        try:
            sellerRef.update(sellerInfo)

        except:
            return jsonify({"code": 404, "message": "Error occured when adding store"})

        return jsonify({"code": 201, "message": "Successfully Updated Information"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
