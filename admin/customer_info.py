from flask import Blueprint, current_app, jsonify, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

Cust, Users, Tickets = dbConnector.Cust, dbConnector.Users, dbConnector.Tickets
admin_customer_info = Blueprint('admin_customer_info', __name__)

@admin_customer_info.route('/customer/<custid>')
def index(custid):
    token = request.cookies.get('access_key')
    if not token:
        return redirect('admin/?redirect=true')

    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        id = int(payload['id'])

        customer = Cust.find_one({'customer_id': int(custid)})
        if not customer:
            return jsonify({"msg": "No or Wrong User is Defined"})

        ticket = Tickets.find({"customer_id": int(custid)})
        tics = [document['ticket_id'] for document in ticket] if ticket else []

        latest_ticket = Tickets.find_one({"customer_id": int(custid)}) or {"subject": "Latest Ticket", 'desc': "No Ticket Found"}
        return render_template('admin/customer_info.html', data=customer, tickets=tics, latest=latest_ticket, custid=custid)

    except jwt.InvalidTokenError:
        return redirect('admin/?redirect=true')
