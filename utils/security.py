import bcrypt


def hash_password(password):
    """
    Hash a plain text password using bcrypt.
    """

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt(rounds=12)

    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode("utf-8")


def verify_password(password, hashed_password):
    """
    Verify a plain text password against a bcrypt hash.
    """

    password_bytes = password.encode("utf-8")

    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_bytes)