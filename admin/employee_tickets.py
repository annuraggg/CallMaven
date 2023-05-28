import jwt
from flask import Blueprint, current_app, redirect, render_template, request
from apis.database_api import Tickets, Cust

employee_tickets = Blueprint('employee_tickets', __name__)

@employee_tickets.route('/tickets/<empid>', methods=['GET', 'POST'])
def index(empid):
    token = request.cookies.get('access_key')
    if not token:
        return redirect('admin/?redirect=true')

    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        tic = Tickets.find({"assigned_to": int(empid)})

        customers = [{
            "ticket_id": doc['ticket_id'],
            "customer_id": doc['customer_id'],
            "subject": doc['subject'],
            "created_at": doc['created_at'],
            "assigned_to": doc['assigned_to'],
            "status": doc['status'].title()
        } for doc in tic]

        if request.method == 'POST':
            ccid = request.form['id']
            if request.form['type'] == "request":
                ticdata = Tickets.find_one({'ticket_id': int(ccid)}, {'_id': 0})
                if ticdata:
                    custdata = Cust.find_one({"customer_id": ticdata['customer_id']})
                    if custdata:
                        tics = {
                            "ticket_id": ticdata['ticket_id'],
                            "name": f"{ticdata['customer_id']} {custdata['fname']} {custdata['lname']}",
                            "subject": ticdata['subject'],
                            "message": ticdata['desc'],
                            "created_at": ticdata['created_at'],
                            "profile": ticdata['customer_id'],
                        }
                        return tics

        return render_template('admin/tickets.html', cust=customers)

    except jwt.InvalidTokenError:
        return redirect('admin/?redirect=true')
