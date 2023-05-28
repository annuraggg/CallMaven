from flask import Blueprint, current_app, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

admin_feedback = Blueprint('admin_feedback', __name__)
Users = dbConnector.Users


@admin_feedback.route('/emp/reviews/<empid>')
def index(empid):
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/admin?redirect=true')
    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        user = Users.find_one({'empid': int(empid)})
        if user:
            arr = []
            for x in user['rating']:
                arr.append(x)

            return render_template('admin/feedback.html', data=arr, jdata={'fname': payload['fname'], 'lname': payload['lname']})
    except jwt.InvalidTokenError:
        pass
    return redirect('/admin?redirect=true')
