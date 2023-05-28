from flask import Blueprint, current_app, jsonify, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

Users = dbConnector.Users
add_call_log = Blueprint('add_call_log', __name__)

@add_call_log.route('/addcall/<custid>', methods=['POST', 'GET'])
def index(custid):
    custid = int(custid)
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/employee?redirect=true')

    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        id = int(payload['id'])
        jdata = {'fname' :payload['fname'], 'lname' : payload['lname']}

        User = Users.find_one({"empid": id})
        if not User:
            return jsonify({"msg": "Role not recognized emp"})

        customer = dbConnector.Cust.find_one({'customer_id': custid})
        if not customer:
            return jsonify({"msg": "Role not recognized cust"})

        phone = int(customer['phone'])

        if request.method == 'POST':
            type, duration, date, time, desc = [request.form.get(k) for k in ['type', 'duration', 'date', 'time', 'desc']]
            if type == "outgoing":
                field = "outgoing_calls"
            elif type == "incoming":
                field = "incoming_calls"
            else:
                return jsonify({"msg": "Type not defined"})
            Users.update_one({"empid": id}, {"$push": {field: {"duration": duration, "date": date, "time": time, "type": type, "from": phone}}})
            Users.update_one({"empid": id}, {"$inc": {"calls_handled.total": 1}})

        return render_template("employee/add_call_log.html", jdata=jdata)

    except jwt.InvalidTokenError:
        return redirect('/employee?redirect=true')
