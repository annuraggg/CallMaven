from flask import Blueprint, current_app, jsonify, redirect, render_template, request
import jwt
import apis.database_api as db

rate = Blueprint('rate', __name__)
Tics = db.Tickets
User = db.Users

@rate.route('/rate/<token>', methods=['GET', 'POST'])
def index(token):
    if request.method == 'POST':
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
            ticket = Tics.find_one({"customer_id": int(payload['custid']), "ticket_id": int(payload['ticket_id'])}, {"_id": 0})
            if ticket:
                rating = int(request.form['rating'])
                feedback = request.form['feedback']
                emp = ticket['assigned_to']
                usr = User.find_one({'empid': emp})
                if usr:
                    User.update_one({'empid': emp}, {"$push": {"rating": {"rating": rating, "feedback": feedback}}})
                    return jsonify("True")
        except jwt.InvalidTokenError:
            return jsonify("Invalid or Expired Token!")
    return render_template('user/rating.html')
