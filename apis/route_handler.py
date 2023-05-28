
from flask import Blueprint
from .logout_api import logout
from .admin_charts_api import admin_charts_api
from .employee_charts_api import employee_charts_api

apis = Blueprint('apis', __name__, url_prefix='/apis')


for bp in [logout, employee_charts_api, admin_charts_api]:
    apis.register_blueprint(bp)
