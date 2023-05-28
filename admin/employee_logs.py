from flask import Blueprint, current_app, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

employee_logs = Blueprint('employee_logs', __name__)
Calls = dbConnector.Calls
Cust = dbConnector.Cust

@employee_logs.route('/logs', methods=['POST', 'GET'])
def index():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/?redirect=true')
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        id = int(payload['id'])
        jdata = {'fname': payload['fname'], 'lname': payload['lname']}
        data = []
        for x in Calls.find({'from': id}):
            if cust := Cust.find_one({"phone": x['to']}):
                data.append({'name': f"{cust['fname']} {cust['lname']}",
                             'phone': cust['phone'],
                             'type': x['direction'],
                             'duration': x['duration'],
                             'time': x['start_time'],
                             'id': cust['customer_id']})
        return render_template("admin/logs.html", logs=data, jdata=jdata)
    except jwt.InvalidTokenError:
        return redirect('/?redirect=true')
