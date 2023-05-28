from flask import Blueprint, current_app, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

feedback = Blueprint('feedback', __name__)
Users = dbConnector.Users

@feedback.route('/feedback')
def feedback_agent():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/employee?redirect=true')
    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        user = Users.find_one({'empid': int(payload['id'])})
        if user:
            arr = []
            for x in user['rating']:
                arr.append(x)

            return render_template('employee/feedback.html', data=arr, jdata={'fname': payload['fname'], 'lname': payload['lname']})
    except jwt.InvalidTokenError:
        pass
    return redirect('/employee?redirect=true')
