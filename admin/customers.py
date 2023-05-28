from flask import Blueprint, current_app, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

admin_customers = Blueprint('admin_customers', __name__)
Customers = dbConnector.Cust

@admin_customers.route('/customers', methods=['POST', 'GET'])
def index():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('admin/?redirect=true')
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        customers = [{'name': f"{doc['fname']} {doc['lname']}", 'phone': doc['phone'], 'email': doc['email'], 'id': doc['customer_id']} for doc in Customers.find({})]
        return render_template('admin/customers.html', customers=customers)
    except jwt.InvalidTokenError:
        return redirect('admin/?redirect=true')
