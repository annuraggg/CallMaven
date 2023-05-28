import datetime
import statistics
from flask import Blueprint, current_app, jsonify, redirect, render_template, request
from apis.database_api import Users, Calls, Tickets
import jwt

admin_employee_info = Blueprint('admin_employee_info', __name__)

@admin_employee_info.route('/employee/<empid>', methods=['POST', 'GET'])
def index(empid):
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/?redirect=true')

    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        user = Users.find_one({'empid': int(empid)})
        data, tickets, calls = {}, [], []

        if user:
            rating = [x['rating'] for x in user['rating']]
            rat = round(statistics.mean(rating), 1) if rating else [0]

            data = {
                'empid': user['empid'],
                'name': user['fname'] + ' ' + user['lname'],
                'email': user['email'],
                'phone': user['phone'],
                'created': user['created_at'],
                'rating': rat,
                'id': empid
            }

            tics = Tickets.find({'assigned_to': int(empid)})
            if tics:
                for x in tics:
                    tickets.append(x['ticket_id'])

                call = Calls.find({"from": int(empid)})
                ist_offset = datetime.timedelta(hours=5, minutes=30)

                if call:
                    for x in call:
                        x['start_time'] = x['start_time'] + ist_offset
                        calls.append(x)

                    sorted_data = sorted(calls, key=lambda k: k['start_time'])

                    return render_template('admin/employee_info.html', data=data, tickets=tickets, jdata={
                        'fname': payload['fname'],
                        'lname': payload['lname']
                    }, calls=sorted_data)

        else:
            return jsonify({"msg": "No user found"})

    except jwt.InvalidTokenError:
        return redirect('/?redirect=true')

    return("Internal Error. Please try again later.")
