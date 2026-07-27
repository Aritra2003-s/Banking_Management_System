from flask import Blueprint, request, Response, flash, redirect, url_for
from controllers.report_controller import reports_controller
from services.report_service import (
    get_customer_report_data,
    get_transaction_report_data,
    get_account_report_data,
    generate_pdf_customer_report,
    generate_excel_transaction_report,
    generate_csv_account_report
)

# Initialize Blueprint
report_bp = Blueprint('report', __name__)


# ==========================================
# 1. MAIN REPORTS DASHBOARD ROUTE
# ==========================================

@report_bp.route('/reports', methods=['GET'])
def reports_route():
    """Renders the consolidated system reports UI dashboard."""
    return reports_controller()


# ==========================================
# 2. EXPORT ROUTES (PDF, EXCEL, CSV)
# ==========================================

@report_bp.route('/reports/customers/pdf', methods=['GET'])
def export_customers_pdf():
    """Step 29: Generates and streams PDF report for customer accounts & net worth."""
    try:
        customers = get_customer_report_data()
        pdf_data = generate_pdf_customer_report(customers)
        return Response(
            pdf_data,
            mimetype="application/pdf",
            headers={"Content-disposition": "attachment; filename=customers_report.pdf"}
        )
    except Exception as e:
        flash(f"Failed to export PDF report: {str(e)}", "danger")
        return redirect(url_for('report.reports_route', tab='customers'))


@report_bp.route('/reports/transactions/excel', methods=['GET'])
def export_transactions_excel():
    """Step 30: Generates and streams Excel (.xlsx) report for transactions."""
    try:
        start_date = request.args.get('start_date', '').strip()
        end_date = request.args.get('end_date', '').strip()
        txn_type = request.args.get('txn_type', 'All').strip()

        transactions = get_transaction_report_data(start_date, end_date, txn_type)
        excel_data = generate_excel_transaction_report(transactions)
        return Response(
            excel_data,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-disposition": "attachment; filename=transactions_report.xlsx"}
        )
    except Exception as e:
        flash(f"Failed to export Excel report: {str(e)}", "danger")
        return redirect(url_for('report.reports_route', tab='transactions'))


@report_bp.route('/reports/accounts/csv', methods=['GET'])
def export_accounts_csv():
    """Step 31: Generates and streams CSV report for bank accounts."""
    try:
        accounts = get_account_report_data()
        csv_data = generate_csv_account_report(accounts)
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=accounts_report.csv"}
        )
    except Exception as e:
        flash(f"Failed to export CSV report: {str(e)}", "danger")
        return redirect(url_for('report.reports_route', tab='accounts'))