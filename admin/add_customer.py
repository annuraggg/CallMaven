from datetime import datetime
import bcrypt
from flask import Blueprint, current_app, jsonify, redirect, render_template, request
import apis.database_api as db
import jwt
Cust = db.Cust
add_customer = Blueprint('add_customer', __name__)


@add_customer.route('/add/customer', methods=['POST', 'GET'])
def index():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/admin/?redirect=true')

    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        id = int(payload['id'])

        if request.method == 'POST':

            last_customer = Cust.find_one(sort=[('customer_id', -1)])
            if last_customer:
                last_customer_id = last_customer['customer_id']
                customer_id = last_customer_id + 1
            else:
                customer_id = 2000

            userobj = {
                "customer_id": customer_id,
                "fname": request.form['fname'],
                "lname": request.form['lname'],
                "email": request.form['email'],
                "phone": request.form['phone'],
            }

            adduser = Cust.insert_one(userobj)

            if adduser:
                redirect('/admin/add/emp?add=true')

        return render_template('admin/add_customer.html')

    except jwt.InvalidTokenError:
        return redirect('/admin/?redirect=true')
