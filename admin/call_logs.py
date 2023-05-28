from flask import Blueprint, current_app, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

admin_call_logs = Blueprint('admin_call_logs', __name__)
Calls, Cust = dbConnector.Calls, dbConnector.Cust

@admin_call_logs.route('/logs/<empid>', methods=['POST', 'GET'])
def index(empid):
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/?redirect=true')
    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        id = int(payload['id'])
        jdata = {'fname' :payload['fname'],
                'lname' : payload['lname']}
        data = []
        call = Calls.find({'from': int(empid)})
        if call:
            for x in call:
                cust = Cust.find_one({"phone": x['to']})
                print(cust)
                if cust:
                    data.append({
                        'name': cust['fname'] + " " + cust['lname'],
                        'phone': cust['phone'],
                        'type': x['direction'],
                        'duration': x['duration'],
                        'time': x['start_time'],
                        'id': cust['customer_id'],
                    })

                
        return render_template("admin/call_logs.html", logs=data, jdata=jdata)
    except jwt.InvalidTokenError:
        return redirect('/admin?redirect=true')
