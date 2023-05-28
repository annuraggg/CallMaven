from flask import Blueprint, current_app, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

admin_employees = Blueprint('admin_employees', __name__)
Users = dbConnector.Users

@admin_employees.route('/employees', methods=['POST', 'GET'])
def index():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/?redirect=true')

    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        customers = [
            {
                "name": f"{doc['fname']} {doc['lname']}",
                "phone": doc['phone'],
                "email": doc['email'],
                "id": doc['empid']
            }
            for doc in Users.find({})
        ]
        return render_template("admin/employees.html", customers=customers)

    except jwt.InvalidTokenError:
        return redirect('/admin/?redirect=true')
