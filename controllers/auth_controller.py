from flask import request, redirect, url_for, flash
from flask_login import login_user, logout_user

from services.auth_service import (
    register_user,
    authenticate_user
)

from models.customer import Customer


# ==========================================
# Register Customer
# ==========================================

def register():

    # Get form data
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    dob = request.form["dob"]
    address = request.form["address"]
    aadhaar = request.form["aadhaar"]
    pan = request.form["pan"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    # Validate passwords
    if password != confirm_password:

        flash("Passwords do not match.", "danger")

        return redirect(url_for("auth.register_page"))

    try:

        register_user(
            first_name,
            last_name,
            email,
            phone,
            dob,
            address,
            aadhaar,
            pan,
            password
        )

        flash("Registration Successful! Please login.", "success")

        return redirect(url_for("auth.login_page"))

    except Exception as e:

        flash(f"Registration Failed: {e}", "danger")

        return redirect(url_for("auth.register_page"))


# ==========================================
# Login Customer
# ==========================================

def login():

    email = request.form["email"]
    password = request.form["password"]

    # Remember Me checkbox
    remember = "remember" in request.form

    user = authenticate_user(email, password)

    if user:

        customer = Customer(user)

        login_user(customer, remember=remember)

        flash("Login Successful!", "success")

        return redirect(url_for("dashboard"))

    flash("Invalid Email or Password.", "danger")

    return redirect(url_for("auth.login_page"))


# ==========================================
# Logout Customer
# ==========================================

def logout():

    logout_user()

    flash("You have been logged out successfully.", "info")

    return redirect(url_for("auth.login_page"))