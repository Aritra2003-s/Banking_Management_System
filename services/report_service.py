from database.database import get_db_connection

def get_customer_report_data():
    """Fetches customer demographic and account distribution metrics."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT 
                c.customer_id,
                c.full_name,
                c.email,
                c.phone,
                c.city,
                COUNT(a.account_id) AS total_accounts,
                COALESCE(SUM(a.balance), 0.00) AS net_worth
            FROM customers c
            LEFT JOIN accounts a ON c.customer_id = a.customer_id
            GROUP BY c.customer_id
            ORDER BY net_worth DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_transaction_report_data(start_date=None, end_date=None, txn_type=None):
    """Fetches filtered transaction history metrics."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT 
                t.transaction_id,
                a.account_number,
                t.transaction_type,
                t.amount,
                t.balance_after,
                t.description,
                t.created_at
            FROM transactions t
            JOIN accounts a ON t.account_id = a.account_id
            WHERE 1=1
        """
        params = []

        if start_date:
            query += " AND t.created_at >= %s"
            params.append(f"{start_date} 00:00:00")

        if end_date:
            query += " AND t.created_at <= %s"
            params.append(f"{end_date} 23:59:59")

        if txn_type and txn_type != 'All':
            query += " AND t.transaction_type = %s"
            params.append(txn_type)

        query += " ORDER BY t.created_at DESC"

        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_account_report_data():
    """Fetches account distribution metrics and overall statistics."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT 
                a.account_id,
                a.account_number,
                c.full_name AS owner_name,
                a.account_type,
                a.balance,
                a.status,
                a.created_at
            FROM accounts a
            JOIN customers c ON a.customer_id = c.customer_id
            ORDER BY a.created_at DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()