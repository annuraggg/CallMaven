from flask import Blueprint, current_app, jsonify, redirect, request
import apis.database_api as dbConnector
import jwt

delete_customer = Blueprint('delete_customer', __name__)
Cust = dbConnector.Cust


@delete_customer.route('/delete/customer/<custid>', methods=['POST', 'GET'])
def index(custid):
    token = request.cookies.get('access_key')
    if not token:
        return redirect('admin/?redirect=true')
    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET'], algorithms=['HS256'])

        if Cust.delete_one({"customer_id": int(custid)}):
            return redirect('/admin/customers')

    except jwt.InvalidTokenError:
        return redirect('/admin/?redirect=true')
    return jsonify({"msg": "Somthing Went Wrong"})
