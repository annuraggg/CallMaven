from flask import Blueprint, jsonify, request
import jwt, bcrypt
from .database_api import Calls, Tickets

calls = Calls
tickets = Tickets
admin_charts_api = Blueprint('admin_charts_api', __name__)

@admin_charts_api.route('/admin/chart1', methods=['POST'])
def index():
    calldur = [document['start_time'] for document in calls.find({})]
    return calldur

@admin_charts_api.route('/admin/chart2', methods=['POST', 'GET'])
def index1():
    ticdur = [document['created_at'] for document in tickets.find({})]
    return ticdur
