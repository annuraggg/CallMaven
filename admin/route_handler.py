from .login import *
from .active_tickets import *
from .tickets import *
from .add_customer import *
from .add_employee import *
from .employees import *
from .customer_info import *
from .admin_dashboard import *
from .customers import *
from .delete_customer import *
from .delete_employee import *
from .employee_info import *
from .employee_logs import *
from .feedback import *
from .call_logs import *
from .employee_tickets import *
from .customer_logs import *
from .categories import *

from flask import Blueprint
admin = Blueprint('admin_main', __name__, url_prefix='/admin')


for bp in [login, active_tickets, tickets, add_customer, add_employee, admin_employees, admin_dashboard,
           admin_customer_info, admin_customers, delete_customer, delete_employee, admin_employee_info, employee_logs, 
           admin_feedback, admin_call_logs, employee_tickets, customer_logs, categories]:
    admin.register_blueprint(bp)

    
