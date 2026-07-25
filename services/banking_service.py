from db import get_db_connection

def deposit_money(account_number, amount, description="Cash Deposit"):
    """
    Executes a deposit operation:
    1. Validates deposit amount and account status.
    2. Updates account balance.
    3. Records transaction history log.
    """
    if amount <= 0:
        return False, "Deposit amount must be greater than zero."

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch account details
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
        account = cursor.fetchone()

        if not account:
            return False, "Account number not found."

        if account['status'] != 'Active':
            return False, f"Cannot deposit. Account status is '{account['status']}'."

        # Calculate new balance
        new_balance = float(account['balance']) + float(amount)

        # Update balance
        cursor.execute(
            "UPDATE accounts SET balance = %s WHERE account_id = %s",
            (new_balance, account['account_id'])
        )

        # Record transaction history log
        cursor.execute(
            """
            INSERT INTO transactions (account_id, transaction_type, amount, balance_after, description)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (account['account_id'], 'Deposit', amount, new_balance, description)
        )

        conn.commit()
        return True, f"Successfully deposited ${amount:,.2f}. New Balance: ${new_balance:,.2f}"

    except Exception as e:
        conn.rollback()
        return False, f"Transaction failed: {str(e)}"

    finally:
        cursor.close()
        conn.close()


def withdraw_money(account_number, amount, description="Cash Withdrawal"):
    """
    Executes a withdrawal operation:
    1. Validates account existence and status.
    2. Checks for sufficient balance.
    3. Updates account balance.
    4. Records transaction history log.
    """
    if amount <= 0:
        return False, "Withdrawal amount must be greater than zero."

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch account details
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
        account = cursor.fetchone()

        if not account:
            return False, "Account number not found."

        if account['status'] != 'Active':
            return False, f"Cannot withdraw. Account status is '{account['status']}'."

        current_balance = float(account['balance'])

        # Check sufficient funds
        if current_balance < amount:
            return False, f"Insufficient funds. Current balance is ${current_balance:,.2f}."

        # Calculate new balance
        new_balance = current_balance - float(amount)

        # Update balance in DB
        cursor.execute(
            "UPDATE accounts SET balance = %s WHERE account_id = %s",
            (new_balance, account['account_id'])
        )

        # Record transaction history log
        cursor.execute(
            """
            INSERT INTO transactions (account_id, transaction_type, amount, balance_after, description)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (account['account_id'], 'Withdrawal', amount, new_balance, description)
        )

        conn.commit()
        return True, f"Successfully withdrew ${amount:,.2f}. Remaining Balance: ${new_balance:,.2f}"

    except Exception as e:
        conn.rollback()
        return False, f"Transaction failed: {str(e)}"

    finally:
        cursor.close()
        conn.close()


def transfer_money(sender_account_no, receiver_account_no, amount, description="Fund Transfer"):
    """
    Executes an atomic transfer operation:
    1. Validates sender and receiver accounts and statuses.
    2. Ensures sender and receiver are distinct accounts.
    3. Checks sender for sufficient funds.
    4. Updates balances for both accounts atomically.
    5. Records debit and credit transaction history logs.
    """
    if amount <= 0:
        return False, "Transfer amount must be greater than zero."

    if sender_account_no == receiver_account_no:
        return False, "Sender and receiver account numbers cannot be the same."

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch sender account
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (sender_account_no,))
        sender = cursor.fetchone()

        if not sender:
            return False, "Sender account number not found."

        if sender['status'] != 'Active':
            return False, f"Sender account status is '{sender['status']}'. Transfer denied."

        sender_balance = float(sender['balance'])
        if sender_balance < amount:
            return False, f"Insufficient funds. Current balance: ${sender_balance:,.2f}"

        # Fetch receiver account
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (receiver_account_no,))
        receiver = cursor.fetchone()

        if not receiver:
            return False, "Receiver account number not found."

        if receiver['status'] != 'Active':
            return False, f"Receiver account status is '{receiver['status']}'. Transfer denied."

        # Calculate new balances
        new_sender_balance = sender_balance - float(amount)
        new_receiver_balance = float(receiver['balance']) + float(amount)

        # Update sender balance (Debit)
        cursor.execute(
            "UPDATE accounts SET balance = %s WHERE account_id = %s",
            (new_sender_balance, sender['account_id'])
        )

        # Update receiver balance (Credit)
        cursor.execute(
            "UPDATE accounts SET balance = %s WHERE account_id = %s",
            (new_receiver_balance, receiver['account_id'])
        )

        # Record sender transaction history log (Transfer Out)
        cursor.execute(
            """
            INSERT INTO transactions (account_id, transaction_type, amount, balance_after, description)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (sender['account_id'], 'Transfer Out', amount, new_sender_balance, f"{description} to {receiver_account_no}")
        )

        # Record receiver transaction history log (Transfer In)
        cursor.execute(
            """
            INSERT INTO transactions (account_id, transaction_type, amount, balance_after, description)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (receiver['account_id'], 'Transfer In', amount, new_receiver_balance, f"{description} from {sender_account_no}")
        )

        conn.commit()
        return True, f"Successfully transferred ${amount:,.2f} to {receiver_account_no}. Remaining Balance: ${new_sender_balance:,.2f}"

    except Exception as e:
        conn.rollback()
        return False, f"Transfer transaction failed: {str(e)}"

    finally:
        cursor.close()
        conn.close()