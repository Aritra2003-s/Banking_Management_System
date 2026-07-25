from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from controllers.account_controller import (
    deposit_controller,
    withdraw_controller,
    transfer_controller,
    mini_statement_controller
)
from services.statement_service import (
    fetch_account_statement,
    generate_csv_statement,
    generate_excel_statement,
    generate_pdf_statement
)

# Initialize Account Blueprint
account_bp = Blueprint('account', __name__)


# ==========================================
# 1. TRANSACTION ROUTES
# ==========================================

@account_bp.route('/deposit', methods=['GET', 'POST'])
def deposit_route():
    """Handles cash deposit transactions."""
    return deposit_controller()


@account_bp.route('/withdraw', methods=['GET', 'POST'])
def withdraw_route():
    """Handles cash withdrawal transactions."""
    return withdraw_controller()


@account_bp.route('/transfer', methods=['GET', 'POST'])
def transfer_route():
    """Handles fund transfers between accounts."""
    return transfer_controller()


# ==========================================
# 2. STATEMENT & REPORT ROUTES
# ==========================================

@account_bp.route('/mini-statement', methods=['GET'])
def mini_statement_route():
    """Displays the recent 5 transactions for a target account."""
    return mini_statement_controller()


@account_bp.route('/statement', methods=['GET'])
def statement_route():
    """Displays full account statements with optional date range filters."""
    account_number = request.args.get('account_number', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    account = None
    transactions = []

    if account_number:
        account, transactions, error = fetch_account_statement(account_number, start_date, end_date)
        if error:
            flash(error, "danger")

    return render_template(
        'statement.html',
        account=account,
        transactions=transactions,
        account_number=account_number,
        start_date=start_date,
        end_date=end_date
    )


@account_bp.route('/statement/export/<export_format>', methods=['GET'])
def export_statement_route(export_format):
    """Exports account statements into PDF, Excel, or CSV format."""
    account_number = request.args.get('account_number', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    if not account_number:
        flash("Account number is required for export.", "danger")
        return redirect(url_for('account.statement_route'))

    account, transactions, error = fetch_account_statement(account_number, start_date, end_date)
    if error or not account:
        flash(error or "Account not found.", "danger")
        return redirect(url_for('account.statement_route'))

    # CSV Export
    if export_format == 'csv':
        data = generate_csv_statement(account, transactions)
        return Response(
            data,
            mimetype="text/csv",
            headers={"Content-disposition": f"attachment; filename=statement_{account_number}.csv"}
        )

    # Excel Export
    elif export_format == 'excel':
        data = generate_excel_statement(account, transactions)
        return Response(
            data,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-disposition": f"attachment; filename=statement_{account_number}.xlsx"}
        )

    # PDF Export
    elif export_format == 'pdf':
        data = generate_pdf_statement(account, transactions)
        return Response(
            data,
            mimetype="application/pdf",
            headers={"Content-disposition": f"attachment; filename=statement_{account_number}.pdf"}
        )

    flash("Invalid export format requested.", "danger")
    return redirect(url_for('account.statement_route'))