import datetime
import jwt
from flask import Blueprint, current_app, jsonify, redirect, render_template, request
from apis.database_api import Tickets, Cust, Users
from apis.mail_api import send_email

tickets = Blueprint('tickets', __name__)


@tickets.route('/activetickets', methods=['GET', 'POST'])
def tickets_agent():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/employee?redirect=true')
    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        id = int(payload['id'])
        jdata = {'fname': payload['fname'], 'lname': payload['lname']}
        tic = Tickets.find({"assigned_to": id, "status": "unresolved"})
        customers = [{"ticket_id": doc['ticket_id'], "customer_id": doc['customer_id'],
                      "subject": doc['subject'], "created_at": doc['created_at']} for doc in tic]
        if request.method == 'POST':
            ccid = request.form['id']
            if request.form['type'] == "request":
                ticdata = Tickets.find_one(
                    {'ticket_id': int(request.form['id'])}, {'_id': 0})
                if ticdata:
                    gmt_time = ticdata['created_at']
                    date = gmt_time + datetime.timedelta(hours=5, minutes=30)
                    custdata = Cust.find_one(
                        {"customer_id": ticdata['customer_id']})
                    if custdata:
                        tics = {"ticket_id": ticdata['ticket_id'], "name": str(ticdata['customer_id']) + " " + custdata['fname'] + " " + custdata['lname'],
                                "subject": ticdata['subject'], "message": ticdata['desc'], "created_at": date, "profile": ticdata['customer_id']}
                        return tics
            elif request.form['type'] == 'resolve':
                desc = request.form['desc']
                time = datetime.datetime.now()
                ticupdate = Tickets.find_one_and_update({'ticket_id': int(request.form['id'])}, {
                                                        "$set": {"status": "resolved", "sol": desc, "updated_at": time}})
                if ticupdate:
                    userupdate = Users.find_one_and_update(
                        {'empid': id}, {"$inc": {"workload": -1}})
                    if userupdate:
                        cusid = int(ticupdate['customer_id'])
                        emailcu = Cust.find_one({"customer_id": cusid})
                        if emailcu:
                            token = jwt.encode(
                                {'custid': emailcu['customer_id'], 'ticket_id': ccid, }, current_app.config['JWT_SECRET'], algorithm='HS256')
                            email = emailcu['email']
                            text = f""" Dear, {email},
                            
Your query with Ticket Number {ccid} has been resolved. Please do not hesitate to reach out to us if you have any further questions or concerns. We would be happy to assist you further. Thank you for choosing our services.

Please Rate Our Services by going to: http://localhost:5000/rate/{token}
Best regards,

CallMaven Team """
                            subject = "[Ticket Resolved] Your query has been resolved"
                            send_email(email, subject, text)
                            return jsonify(True)
        return render_template('employee/tickets.html', cust=customers, jdata=jdata)
    except (jwt.InvalidTokenError, KeyError):
        return redirect('/employee?redirect=true')
