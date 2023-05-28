from datetime import datetime
from flask import Blueprint, current_app, redirect, render_template, request
import jwt
import apis.database_api as dbConnector

admin_dashboard = Blueprint('admin_dashboard', __name__)
Users, Tickets = dbConnector.Users, dbConnector.Tickets

@admin_dashboard.route('/dashboard')
def index():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/admin?redirect=true')

    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        user_id = int(payload['id'])
        return render_template('admin/dashboard.html', data=[], calls=[])
    except jwt.InvalidTokenError:
        return redirect('/?redirect=true')
