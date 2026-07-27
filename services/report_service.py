import csv
import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from database.database import get_db_connection


# ==========================================
# 1. DATA FETCHING FUNCTIONS
# ==========================================

def get_customer_report_data():
    """Fetches customer demographics and financial totals."""
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
    """Fetches transaction records with optional filters."""
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
    """Fetches account list and owner metrics."""
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


# ==========================================
# 2. STEP 29: GENERATE PDF CUSTOMER REPORT
# ==========================================

def generate_pdf_customer_report(customers):
    """Generates an official PDF report of customer net worth and accounts."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=12
    )
    elements.append(Paragraph("Secure Bank - Executive Customer Report", title_style))
    elements.append(Spacer(1, 10))

    # Table Header & Rows
    table_data = [["ID", "Full Name", "Email", "City", "Accounts", "Net Worth"]]
    for c in customers:
        table_data.append([
            f"#{c['customer_id']}",
            c['full_name'],
            c['email'],
            c['city'] or 'N/A',
            str(c['total_accounts']),
            f"${float(c['net_worth']):,.2f}"
        ])

    table = Table(table_data, colWidths=[40, 120, 140, 80, 60, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


# ==========================================
# 3. STEP 30: GENERATE EXCEL TRANSACTIONS REPORT
# ==========================================

def generate_excel_transaction_report(transactions):
    """Generates an Excel (.xlsx) workbook of system transactions."""
    df_data = []
    for t in transactions:
        df_data.append({
            "Transaction ID": t['transaction_id'],
            "Account Number": t['account_number'],
            "Type": t['transaction_type'],
            "Amount ($)": float(t['amount']),
            "Balance After ($)": float(t['balance_after']),
            "Description": t['description'] or 'N/A',
            "Date & Time": str(t['created_at'])
        })

    if df_data:
        df = pd.DataFrame(df_data)
    else:
        df = pd.DataFrame(columns=[
            "Transaction ID", "Account Number", "Type", 
            "Amount ($)", "Balance After ($)", "Description", "Date & Time"
        ])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Transactions')

    output.seek(0)
    return output.getvalue()


# ==========================================
# 4. STEP 31: GENERATE CSV ACCOUNTS REPORT
# ==========================================

def generate_csv_account_report(accounts):
    """Generates a CSV file containing all account details."""
    output = io.StringIO()
    writer = csv.writer(output)

    # File Header
    writer.writerow(["Secure Bank - System Accounts Report"])
    writer.writerow([])
    writer.writerow(["Account ID", "Account Number", "Owner Name", "Type", "Balance ($)", "Status", "Created At"])

    for a in accounts:
        writer.writerow([
            a['account_id'],
            a['account_number'],
            a['owner_name'],
            a['account_type'],
            f"{float(a['balance']):.2f}",
            a['status'],
            str(a['created_at'])
        ])

    output.seek(0)
    return output.getvalue().encode('utf-8')