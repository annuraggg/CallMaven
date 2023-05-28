import datetime
from flask import Blueprint, current_app, redirect, render_template, request
import jwt
import apis.database_api as dbConnector
import statistics

dashboard = Blueprint('dashboard', __name__)
Users, Tickets, Calls = dbConnector.Users, dbConnector.Tickets, dbConnector.Calls


@dashboard.route('/dashboard')
def dashboard_agent():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/employee?redirect=true')

    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        user_id = int(payload['id'])
        jdata = {'fname': payload['fname'],
                 'lname': payload['lname']}

        user = Users.find_one({"empid": user_id})
        if not user:
            return redirect('/employee?redirect=true')

        today = datetime.datetime.now().date()
        print(today)
        tickets_cursor = Tickets.find({'assigned_to': user_id})
        tic = 0

        date_format = "%d-%m-%Y"
        for x in tickets_cursor:
            x['created_at'] = datetime.datetime.strptime(
                x['created_at'], date_format).date()
            if (x['created_at'] == today):
                tic += 1

        print("TICKETS", tic)

        tickets_cursor1 = Tickets.find(
            {'assigned_to': user_id, 'status': 'unresolved'})
        ticun = 0
        for x in tickets_cursor1:
            x['created_at'] = x['created_at'].date()
            if (x['created_at'] == today):
                ticun += 1

        data = []
        call = Calls.find({'from': user_id})
        calls = []
        if call:
            for x in call:
                gmt_time = x['start_time']
                date = gmt_time + datetime.timedelta(hours=5, minutes=30)
                calls.append({
                    'type': x['direction'],
                    'duration': x['duration'],
                    'time': date,
                })

            calls.sort(key=lambda x: x['time'])

        rating = []
        for x in user['rating']:
            print(x['rating'])
            rating.append(x['rating'])

        if rating:
            rat = x = round(statistics.mean(rating), 1)
        else:
            rat = [0]

        data = {
            'name': user['fname'],
            'lname': user['lname'],
            'rating': rat,
            'totaltickets': tic,
            'totalcalls': len(calls),
            'unresolved': ticun,
            'id': user['empid']
        }

        return render_template('employee/dashboard.html', data=data, calls=calls, jdata=jdata)

    except jwt.InvalidTokenError:
        return redirect('/employee?redirect=true')
