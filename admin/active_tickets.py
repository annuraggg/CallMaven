import jwt
from flask import Blueprint, current_app, redirect, render_template, request
from apis.database_api import Tickets, Cust
from apis.mail_api import send_email

active_tickets = Blueprint('aticketsactive', __name__)


@active_tickets.route('/activetickets', methods=['GET', 'POST'])
def index():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/?redirect=true')

    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        tic = Tickets.find({"status": "unresolved"})
        customers = [{"ticket_id": doc['ticket_id'], "customer_id": doc['customer_id'],
                      "subject": doc['subject'], "created_at": doc['created_at']} for doc in tic]

        if request.method == 'POST':
            ticdata = Tickets.find_one(
                {'ticket_id': int(request.form['id'])}, {'_id': 0})
    
            if ticdata:
                custdata = Cust.find_one(
                    {"customer_id": ticdata['customer_id']})

                if custdata:
                    tics = {"ticket_id": ticdata['ticket_id'], "name": str(ticdata['customer_id']) + " " + custdata['fname'] + " " + custdata['lname'],
                            "subject": ticdata['subject'], "message": ticdata['desc'], "created_at": ticdata['created_at'], "profile": ticdata['customer_id']}
                    return tics

        return render_template('admin/active_tickets.html', cust=customers)

    except (jwt.InvalidTokenError, KeyError):
        return redirect('/?redirect=true')
