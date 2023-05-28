from apis.database_api import Tickets, Users, Cust
from flask import Blueprint, redirect, render_template, request
from datetime import datetime
from apis.mail_api import send_email

support = Blueprint('support', __name__)


@support.route('/support', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        custid, subject, message = map(
            request.form.get, ['custid', 'subject', 'message'])
        last_ticket = Tickets.find_one(sort=[('ticket_id', -1)])
        last_id = (last_ticket['ticket_id'] + 1) if last_ticket else 1000
        lowest_load = Users.find_one(sort=[('workload', 1)])[  # type: ignore
            'empid'] if Users.find_one(sort=[('workload', 1)]) else None
        customer = Cust.find_one({"customer_id": int(request.form['custid'])})
        email, fname = (customer['email'],
                        customer['fname']) if customer else ("", "")
        current_date = datetime.utcnow()
        ticket = {
            'ticket_id': last_id,
            'customer_id': int(custid),  # type: ignore
            'subject': subject,
            'desc': message,
            'assigned_to': lowest_load,
            'status': "unresolved",
            'created_at': current_date,
            'updated_at': current_date
        }

        if Tickets.insert_one(ticket) and Users.update_one({'empid': lowest_load}, {'$inc': {'workload': 1}}):

            text = f"""
Dear {fname},
We would like to confirm that we have received your request for assistance with {subject}. A ticket for your issue has been created with the Ticket No: {last_id} and our team is actively working to resolve it as quickly as possible. We will keep you informed of any updates regarding your ticket, and if we require any additional information, we will contact you promptly. Please do not hesitate to contact us if you have any further questions or concerns.
Best regards,
CallMaven Support Team"""

            send_email(email, "Ticket Raised", text)
            return redirect('support?raised=true') if True else redirect('support?error=true')
        else:
            return redirect('support?error=true')
    return render_template('user/support.html')
