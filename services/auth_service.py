from database.database import get_connection
from utils.security import hash_password, verify_password


# ==========================================
# Register New Customer
# ==========================================

def register_user(
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

        # Hash password before saving
        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO Customer (
                first_name,
                last_name,
                email,
                phone,
                date_of_birth,
                address,
                aadhaar,
                pan,
                password
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                first_name,
                last_name,
                email,
                phone,
                dob,
                address,
                aadhaar,
                pan,
                hashed_password
            )
        )

        conn.commit()

    except Exception as e:

        conn.rollback()

        raise e

    finally:

        conn.close()


# ==========================================
# Authenticate Customer
# ==========================================

def authenticate_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM Customer
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    # Customer not found
    if user is None:
        return None

    # Verify hashed password
    if verify_password(password, user["password"]):
        return user

    return None