import datetime
from flask import Blueprint, current_app, jsonify, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

Cust, Users, Tickets, Calls = dbConnector.Cust, dbConnector.Users, dbConnector.Tickets, dbConnector.Calls
cust_info = Blueprint('cust_info', __name__)


@cust_info.route('/customer/<custid1>')
def cust_inf(custid1):
    token1 = request.cookies.get('access_key')
    if not token1:
        return redirect('/employee?redirect=true')
    try:
        payload = jwt.decode(
            token1, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        id = int(payload['id'])
        jdata = {'fname': payload['fname'], 'lname': payload['lname']}
        customer = Cust.find_one({'customer_id': int(custid1)})
        if customer:
            user = Users.find_one({"empid": int(id)})
            phone = customer['phone']
            call = Calls.find({"from": id, "to": phone})
            ist_offset = datetime.timedelta(hours=5, minutes=30)
            if customer and user and call:
                sorted_data = sorted([{'start_time': x['start_time'] + ist_offset}
                                    for x in call], key=lambda k: k['start_time'])
                ticket = Tickets.find(
                    {"customer_id": int(custid1), "assigned_to": int(id)})
                if ticket:
                    tics = [document['ticket_id'] for document in ticket]
                    latest_ticket = Tickets.find_one({"customer_id": int(custid1), "assigned_to": int(id)}) or {
                        "subject": "No Tickets Found", "desc": ""}
                    return render_template('employee/customer_info.html', data=customer, calls=sorted_data, tickets=tics, latest=latest_ticket, id=id, jdata=jdata)
            return jsonify({"msg": "No or Wrong User is Defined"})
    except jwt.InvalidTokenError:
        return redirect('/employee?redirect=true')
