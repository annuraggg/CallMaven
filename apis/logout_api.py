from flask import Blueprint, current_app, jsonify, redirect, render_template, request
import jwt

logout = Blueprint('logout', __name__)

@logout.route('/logout')
def index():
    return render_template('logout.html')
