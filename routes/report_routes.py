from flask import Blueprint
from controllers.report_controller import reports_controller

report_bp = Blueprint('report', __name__)

@report_bp.route('/reports', methods=['GET'])
def reports_route():
    """Renders the consolidated system reports panel."""
    return reports_controller()