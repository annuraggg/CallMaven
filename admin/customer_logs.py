from flask import Blueprint, current_app, jsonify, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

customer_logs = Blueprint('customer_logs', __name__)
Calls = dbConnector.Calls
Cust = dbConnector.Cust


@customer_logs.route('/customer/logs/<cusid>', methods=['POST', 'GET'])
def index(cusid):
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/?redirect=true')
    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        id = int(payload['id'])
        jdata = {'fname': payload['fname'], 'lname': payload['lname']}
        data = []

        cust = Cust.find_one({"customer_id": int(cusid)})
        if cust:
            phone = cust['phone']

            for x in Calls.find({'to': phone}):
                data.append({'name': f"{cust['fname']} {cust['lname']}",
                            'phone': cust['phone'],
                             'type': x['direction'],
                             'duration': x['duration'],
                             'time': x['start_time'],
                             'id': cust['customer_id']})
            return render_template("admin/call_logs.html", logs=data, jdata=jdata)
        else:
            return jsonify({'error': 'Record not found'})
    except jwt.InvalidTokenError:
        return redirect('/?redirect=true')
