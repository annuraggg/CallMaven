from flask import Blueprint, current_app, redirect, request
import apis.database_api as dbConnector
import jwt

delete_employee = Blueprint('delete_employee', __name__)
User = dbConnector.Users

@delete_employee.route('delete/employee/<empid>', methods=['POST', 'GET'])
def index(empid):
    token = request.cookies.get('access_key')
    if not token:
        return redirect('admin/?redirect=true')

    try:
        jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        User.delete_one({"empid": int(empid)})
        return redirect('/admin/employees')

    except jwt.InvalidTokenError:
        return redirect('/admin/?redirect=true')

