from database.database import get_connection
from utils.security import hash_password


# ==========================================
# Get All Customers
# ==========================================

def get_all_customers():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT *
            FROM Customer
            ORDER BY customer_id DESC
        """)

        customers = cursor.fetchall()

        return customers

    finally:

        conn.close()


# ==========================================
# Get Customer By ID
# ==========================================

def get_customer_by_id(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT *
            FROM Customer
            WHERE customer_id = ?
        """, (customer_id,))

        customer = cursor.fetchone()

        return customer

    finally:

        conn.close()


# ==========================================
# Add Customer
# ==========================================

def add_customer(
    first_name,
    last_name,
    email,
    phone,
    dob,
    address,
    aadhaar,
    pan,
    password
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO Customer(
                first_name,
                last_name,
                email,
                phone,
                date_of_birth,
                address,
                aadhaar,
                pan,
                password,
                status
            )

            VALUES(
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )

        """, (

            first_name,
            last_name,
            email,
            phone,
            dob,
            address,
            aadhaar,
            pan,
            hashed_password,
            "Active"

        ))

        conn.commit()

    except Exception as e:

        conn.rollback()

        raise e

    finally:

        conn.close()


# ==========================================
# Update Customer
# ==========================================

def update_customer(

    customer_id,
    first_name,
    last_name,
    email,
    phone,
    dob,
    address,
    aadhaar,
    pan

):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""

            UPDATE Customer

            SET

                first_name = ?,
                last_name = ?,
                email = ?,
                phone = ?,
                date_of_birth = ?,
                address = ?,
                aadhaar = ?,
                pan = ?

            WHERE customer_id = ?

        """, (

            first_name,
            last_name,
            email,
            phone,
            dob,
            address,
            aadhaar,
            pan,
            customer_id

        ))

        conn.commit()

    except Exception as e:

        conn.rollback()

        raise e

    finally:

        conn.close()


# ==========================================
# Search Customers
# ==========================================

def search_customers(keyword):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        search = f"%{keyword}%"

        cursor.execute("""

            SELECT *

            FROM Customer

            WHERE

            first_name LIKE ?

            OR

            last_name LIKE ?

            OR

            email LIKE ?

            OR

            phone LIKE ?

            OR

            aadhaar LIKE ?

            OR

            pan LIKE ?

            ORDER BY customer_id DESC

        """, (

            search,
            search,
            search,
            search,
            search,
            search

        ))

        customers = cursor.fetchall()

        return customers

    finally:

        conn.close()


# ==========================================
# Freeze Customer
# ==========================================

def freeze_customer(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""

            UPDATE Customer

            SET status = 'Frozen'

            WHERE customer_id = ?

        """, (

            customer_id,

        ))

        conn.commit()

    except Exception as e:

        conn.rollback()

        raise e

    finally:

        conn.close()


# ==========================================
# Activate Customer
# ==========================================

def activate_customer(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""

            UPDATE Customer

            SET status = 'Active'

            WHERE customer_id = ?

        """, (

            customer_id,

        ))

        conn.commit()

    except Exception as e:

        conn.rollback()

        raise e

    finally:

        conn.close()


# ==========================================
# Soft Delete Customer
# ==========================================

def delete_customer(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""

            UPDATE Customer

            SET status = 'Deleted'

            WHERE customer_id = ?

        """, (

            customer_id,

        ))

        conn.commit()

    except Exception as e:

        conn.rollback()

        raise e

    finally:

        conn.close()