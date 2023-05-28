from flask import Blueprint, current_app, jsonify, render_template, request
import jwt, apis.database_api as db
import bcrypt

Users = db.Users
login = Blueprint('login', __name__)

@login.route('/', methods=['POST', 'GET'])
def login_agent():

    if request.method == 'POST':
        id, pw = int(request.form['cid']), request.form['pw']
        user = Users.find_one({"empid": id})

        if user and bcrypt.checkpw(pw.encode(), user['password'].encode()):
            token = jwt.encode({'id': id, 'fname': user['fname'], 'lname': user['lname']}, 
                               current_app.config['JWT_SECRET'], algorithm='HS256')
            return jsonify({'token': token, "auth": "True"})
        return jsonify({"auth": "False"})

    return render_template('employee/login.html')
