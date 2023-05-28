from datetime import datetime
import bcrypt
from flask import Blueprint, current_app, jsonify, redirect, render_template, request
import apis.database_api as dbConnector
import jwt
Users = dbConnector.Users
add_employee = Blueprint('addemp', __name__)

@add_employee.route('/add/employee', methods=['POST', 'GET'])
def index():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('admin/?redirect=true')
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        id = int(payload['id'])
        if request.method == 'POST':
            fname, lname, email, phone = request.form['fname'], request.form['lname'], request.form['email'], request.form['phone']
            last_id = Users.find_one(sort=[('empid', -1)])
            last_no = (last_id['empid'] + 1) if last_id else 22200000
            
            upw = request.form['pw']
            salt = bcrypt.gensalt(12)
            pw = bcrypt.hashpw(upw.encode('utf-8'), salt)
            apw = pw.decode('utf-8')

            userobj = {
                "empid": last_no,
                "fname": fname,
                "lname": lname,
                "email": email,
                "phone": phone,
                "password": apw,
                "created_at": datetime.now(),
                "workload": 0,
                "rating": [],
                "default": True
            }
            adduser = Users.insert_one(userobj)
            if adduser:
                redirect('/admin/add/emp?add=true')
        return render_template('admin/add_employee.html ')
    except jwt.InvalidTokenError:
        return redirect('admin/?redirect=true')
