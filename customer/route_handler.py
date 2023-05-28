from flask import Blueprint, Flask
from .rate import *
from .support import *
customer = Blueprint('customer', __name__, url_prefix='/')


for bp in [rate, support]:
    customer.register_blueprint(bp)
