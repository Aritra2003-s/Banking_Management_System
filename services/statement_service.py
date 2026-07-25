import csv
import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from db import get_db_connection


def fetch_account_statement(account_number, start_date=None, end_date=None):
    """
    Fetches account details and transaction history filtered by optional date range.
    
    Returns:
        tuple: (account_dict, transactions_list, error_message)
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch target account
        cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
        account = cursor.fetchone()

        if not account:
            return None, None, "Account number not found."

        # Base transaction query
        query = """
            SELECT transaction_id, transaction_type, amount, balance_after, description, created_at
            FROM transactions
            WHERE account_id = %s
        """
        params = [account['account_id']]

        # Apply optional date range filters
        if start_date:
            query += " AND created_at >= %s"
            params.append(f"{start_date} 00:00:00")

        if end_date:
            query += " AND created_at <= %s"
            params.append(f"{end_date} 23:59:59")

        query += " ORDER BY created_at DESC"

        cursor.execute(query, tuple(params))
        transactions = cursor.fetchall()

        return account, transactions, None

    except Exception as e:
        return None, None, f"Database query error: {str(e)}"

    finally:
        cursor.close()
        conn.close()


def generate_csv_statement(account, transactions):
    """Generates a downloadable CSV account statement."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Statement Metadata Header
    writer.writerow(["Secure Bank - Account Statement"])
    writer.writerow(["Account Number:", account['account_number']])
    writer.writerow(["Current Balance:", f"${float(account['balance']):,.2f}"])
    writer.writerow([])
    
    # Table Column Headers
    writer.writerow(["Txn ID", "Type", "Amount ($)", "Balance After ($)", "Description", "Date & Time"])

    # Transaction Rows
    for txn in transactions:
        writer.writerow([
            txn['transaction_id'],
            txn['transaction_type'],
            f"{float(txn['amount']):.2f}",
            f"{float(txn['balance_after']):.2f}",
            txn['description'] or '',
            str(txn['created_at'])
        ])

    output.seek(0)
    return output.getvalue().encode('utf-8')


def generate_excel_statement(account, transactions):
    """Generates a downloadable Excel (.xlsx) account statement."""
    df_data = []
    
    for txn in transactions:
        df_data.append({
            "Transaction ID": txn['transaction_id'],
            "Type": txn['transaction_type'],
            "Amount ($)": float(txn['amount']),
            "Balance After ($)": float(txn['balance_after']),
            "Description": txn['description'] or '',
            "Date & Time": str(txn['created_at'])
        })

    # Create DataFrame or handle empty state gracefully
    if df_data:
        df = pd.DataFrame(df_data)
    else:
        df = pd.DataFrame(columns=["Transaction ID", "Type", "Amount ($)", "Balance After ($)", "Description", "Date & Time"])

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Statement')

    output.seek(0)
    return output.getvalue()


def generate_pdf_statement(account, transactions):
    """Generates a styled, printable PDF account statement using ReportLab."""
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

    # Title Banner
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=10
    )
    elements.append(Paragraph("Secure Bank - Official Account Statement", title_style))
    elements.append(Spacer(1, 10))

    # Account Details Summary Header
    account_balance = float(account['balance'])
    info_text = f"<b>Account Number:</b> {account['account_number']}<br/><b>Current Balance:</b> ${account_balance:,.2f}"
    elements.append(Paragraph(info_text, styles['Normal']))
    elements.append(Spacer(1, 15))

    # Table Data Formatting
    table_data = [["Txn ID", "Type", "Amount", "Balance After", "Date"]]
    
    if transactions:
        for txn in transactions:
            table_data.append([
                f"#{txn['transaction_id']}",
                txn['transaction_type'],
                f"${float(txn['amount']):,.2f}",
                f"${float(txn['balance_after']):,.2f}",
                str(txn['created_at'])[:10]
            ])
    else:
        table_data.append(["N/A", "No records", "$0.00", "$0.00", "N/A"])

    # Table Layout & Styling
    table = Table(table_data, colWidths=[60, 100, 90, 100, 100])
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