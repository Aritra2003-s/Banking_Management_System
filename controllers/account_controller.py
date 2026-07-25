from flask import render_template, request, redirect, url_for, flash
from db import get_db_connection
from services.banking_service import (
    deposit_money,
    withdraw_money,
    transfer_money
)

def deposit_controller():
    """Handles deposit requests, input validation, and rendering deposit.html."""
    if request.method == 'POST':
        account_number = request.form.get('account_number', '').strip()
        amount_raw = request.form.get('amount', '').strip()
        description = request.form.get('description', 'Cash Deposit').strip()

        # Validate required inputs
        if not account_number:
            flash("Account number is required.", "danger")
            return render_template('deposit.html')

        try:
            amount = float(amount_raw)
        except ValueError:
            flash("Invalid amount entered. Please enter a valid number.", "danger")
            return render_template('deposit.html')

        # Execute transaction via Service Layer
        success, message = deposit_money(account_number, amount, description)

        if success:
            flash(message, "success")
            return redirect(url_for('account.deposit_route'))
        else:
            flash(message, "danger")

    return render_template('deposit.html')


def withdraw_controller():
    """Handles withdrawal requests, input validation, and rendering withdraw.html."""
    if request.method == 'POST':
        account_number = request.form.get('account_number', '').strip()
        amount_raw = request.form.get('amount', '').strip()
        description = request.form.get('description', 'Cash Withdrawal').strip()

        # Validate required inputs
        if not account_number:
            flash("Account number is required.", "danger")
            return render_template('withdraw.html')

        try:
            amount = float(amount_raw)
        except ValueError:
            flash("Invalid amount entered. Please enter a valid numerical value.", "danger")
            return render_template('withdraw.html')

        # Execute transaction via Service Layer
        success, message = withdraw_money(account_number, amount, description)

        if success:
            flash(message, "success")
            return redirect(url_for('account.withdraw_route'))
        else:
            flash(message, "danger")

    return render_template('withdraw.html')


def transfer_controller():
    """Handles fund transfer requests between accounts and rendering transfer.html."""
    if request.method == 'POST':
        sender_account_no = request.form.get('sender_account_no', '').strip()
        receiver_account_no = request.form.get('receiver_account_no', '').strip()
        amount_raw = request.form.get('amount', '').strip()
        description = request.form.get('description', 'Fund Transfer').strip()

        # Validate required inputs
        if not sender_account_no or not receiver_account_no:
            flash("Both sender and receiver account numbers are required.", "danger")
            return render_template('transfer.html')

        try:
            amount = float(amount_raw)
        except ValueError:
            flash("Invalid transfer amount entered. Please enter a valid number.", "danger")
            return render_template('transfer.html')

        # Execute transaction via Service Layer
        success, message = transfer_money(sender_account_no, receiver_account_no, amount, description)

        if success:
            flash(message, "success")
            return redirect(url_for('account.transfer_route'))
        else:
            flash(message, "danger")

    return render_template('transfer.html')


def mini_statement_controller():
    """Fetches recent 5 transactions for an account and renders mini_statement.html."""
    account_number = request.args.get('account_number', '').strip()
    transactions = []
    account = None

    if account_number:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Verify Account
            cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
            account = cursor.fetchone()

            if account:
                # Fetch last 5 transactions
                cursor.execute("""
                    SELECT transaction_id, transaction_type, amount, balance_after, description, created_at
                    FROM transactions
                    WHERE account_id = %s
                    ORDER BY created_at DESC
                    LIMIT 5
                """, (account['account_id'],))
                transactions = cursor.fetchall()
            else:
                flash("Account number not found.", "danger")

        finally:
            cursor.close()
            conn.close()

    return render_template(
        'mini_statement.html',
        account=account,
        transactions=transactions,
        account_number=account_number
    )