from flask import render_template, request
from services.report_service import (
    get_customer_report_data,
    get_transaction_report_data,
    get_account_report_data
)

def reports_controller():
    """Handles data fetching for the consolidated reporting dashboard."""
    active_tab = request.args.get('tab', 'customers')
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    txn_type = request.args.get('txn_type', 'All').strip()

    customers_data = get_customer_report_data()
    transactions_data = get_transaction_report_data(start_date, end_date, txn_type)
    accounts_data = get_account_report_data()

    # Calculate Summary Totals
    total_customers = len(customers_data)
    total_accounts = len(accounts_data)
    total_liquidity = sum(float(acc['balance']) for acc in accounts_data)
    total_volume = sum(float(txn['amount']) for txn in transactions_data)

    return render_template(
        'reports.html',
        active_tab=active_tab,
        customers=customers_data,
        transactions=transactions_data,
        accounts=accounts_data,
        start_date=start_date,
        end_date=end_date,
        txn_type=txn_type,
        total_customers=total_customers,
        total_accounts=total_accounts,
        total_liquidity=total_liquidity,
        total_volume=total_volume
    )