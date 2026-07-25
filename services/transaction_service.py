from database.database import get_db_connection

def record_transaction(account_id, transaction_type, amount, balance_after, description=""):
    """
    Inserts a standalone transaction record into the database log.

    Args:
        account_id (int): ID of the account associated with the transaction.
        transaction_type (str): Type of transaction (e.g., 'Deposit', 'Withdrawal', 'Transfer Out', 'Transfer In').
        amount (float): Transaction amount.
        balance_after (float): Account balance immediately after execution.
        description (str, optional): Additional note or reference details. Defaults to "".
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO transactions (account_id, transaction_type, amount, balance_after, description)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (account_id, transaction_type, amount, balance_after, description)
        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()