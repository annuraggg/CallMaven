from flask import Blueprint, current_app, jsonify, render_template, request
import jwt
from apis.database_api import Admin as Adm
import bcrypt

login = Blueprint('admin_login', __name__)

@login.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        id, pw = int(request.form['cid']), request.form['pw']
        user = Adm.find_one({"username": id})
        if user and bcrypt.checkpw(pw.encode('utf-8'), user['password'].encode('utf-8')):
            token = jwt.encode(
                {'id': id,
                 'fname': user['fname'],
                 'lname': user['lname']}, current_app.config['JWT_SECRET'], algorithm='HS256')
            return jsonify({'token': token, "auth": "True"})
        return jsonify({"auth": "False"})
    return render_template('admin/login.html')
