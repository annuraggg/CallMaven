from flask import Blueprint, current_app, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

customers = Blueprint('customers', __name__)
Customers = dbConnector.Cust
User = dbConnector.Users


@customers.route('/customers', methods=['POST', 'GET'])
def customers_agent():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/employee?redirect=true')
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        id = int(payload['id'])
        jdata = {'fname': payload['fname'], 'lname': payload['lname']}

        customers = [{"name": f"{doc['fname']} {doc['lname']}", "phone": doc['phone'],
                      "email": doc['email'], "id": doc['customer_id']} for doc in Customers.find({})]
        return render_template("employee/customers.html", customers=customers, jdata=jdata)
    except jwt.InvalidTokenError:
        return redirect('/employee?redirect=true')
