from flask import Blueprint, request
from .database_api import Tickets, Calls
calls = Calls
tickets = Tickets
employee_charts_api = Blueprint('employee_charts_api', __name__)


@employee_charts_api.route('employee/chart1', methods=['POST'])
def index():
    calldur = []
    if request.method == 'POST':
        id = int(request.form['empid'])
        call = calls.find({'from': id})
        calldur = [document['start_time'] for document in call]

    return calldur


@employee_charts_api.route('employee/chart2', methods=['POST', 'GET'])
def index1():
    ticdur = []
    if request.method == 'POST':
        id = int(request.form['empid'])
        tics = tickets.find({'assigned_to': id})
        ticdur = [document['created_at'] for document in tics]

    return ticdur
