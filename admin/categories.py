from flask import Blueprint, current_app, jsonify, redirect, render_template, request
import apis.database_api as dbConnector
import jwt

categories = Blueprint('categories', __name__)
Calls, Cust = dbConnector.Calls, dbConnector.Cust


@categories.route('/categories', methods=['POST', 'GET'])
def index():
    token = request.cookies.get('access_key')
    if not token:
        return redirect('/?redirect=true')
    try:
        payload = jwt.decode(
            token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        cat = dbConnector.Categories.find({})
        categories = []
        for x in cat:
            categories.append({
                'id': x['id'],
                'name': x['name'],
            })

        if request.method == 'POST':
            if request.form['type'] == 'delete':
                id = int(request.form['id'])
                delete = dbConnector.Categories.delete_one({'id': id})
                if delete:
                    return jsonify({'status': 'success'})

            if request.form['type'] == 'add':
                name = request.form['name']
                desc = request.form['desc']

                add = dbConnector.Categories.insert_one({
                    'id': categories[-1]['id'] + 1,
                    'name': name,
                    'desc': desc
                })
                if add:
                    return jsonify({'status': 'success'})

        return render_template("admin/categories.html", categories=categories)
    except jwt.InvalidTokenError:
        return redirect('/admin?redirect=true')
