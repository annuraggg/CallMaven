from flask import Blueprint, Flask
from .add_call_log import add_call_log
from .call_logs import call_logs
from .cust_info import cust_info
from .customers import customers
from .dashboard import dashboard
from .feedback import feedback
from .login import login
from .tickets import tickets

employee = Blueprint('employee', __name__, url_prefix='/employee')

for bp in [add_call_log, call_logs, cust_info, customers, dashboard, feedback, login, tickets]:
    employee.register_blueprint(bp)
