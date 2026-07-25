from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from services.customer_service import (
    get_all_customers,
    get_customer_by_id,
    add_customer,
    update_customer,
    search_customers,
    freeze_customer,
    activate_customer,
    delete_customer
)


# ==========================================
# Display All Customers
# ==========================================

def customers():

    customer_list = get_all_customers()

    return render_template(
        "customers.html",
        customers=customer_list
    )


# ==========================================
# Show Add Customer Page
# ==========================================

def add_customer_page():

    return render_template("add_customer.html")


# ==========================================
# Add Customer
# ==========================================

def add_customer_controller():

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    dob = request.form["dob"]
    address = request.form["address"]
    aadhaar = request.form["aadhaar"]
    pan = request.form["pan"]
    password = request.form["password"]

    try:

        add_customer(
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

        flash("Customer added successfully.", "success")

        return redirect(url_for("customer.customers"))

    except Exception as e:

        flash(f"Error: {e}", "danger")

        return redirect(url_for("customer.add_customer_page"))


# ==========================================
# Show Edit Customer Page
# ==========================================

def edit_customer_page(customer_id):

    customer = get_customer_by_id(customer_id)

    if customer is None:

        flash("Customer not found.", "warning")

        return redirect(url_for("customer.customers"))

    return render_template(
        "edit_customer.html",
        customer=customer
    )


# ==========================================
# Update Customer
# ==========================================

def update_customer_controller(customer_id):

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    dob = request.form["dob"]
    address = request.form["address"]
    aadhaar = request.form["aadhaar"]
    pan = request.form["pan"]

    try:

        update_customer(
            customer_id,
            first_name,
            last_name,
            email,
            phone,
            dob,
            address,
            aadhaar,
            pan
        )

        flash("Customer updated successfully.", "success")

        return redirect(url_for("customer.customers"))

    except Exception as e:

        flash(f"Error: {e}", "danger")

        return redirect(
            url_for(
                "customer.edit_customer_page",
                customer_id=customer_id
            )
        )


# ==========================================
# Search Customer
# ==========================================

def search_customer():

    keyword = request.args.get("search", "").strip()

    if keyword == "":

        return redirect(url_for("customer.customers"))

    customer_list = search_customers(keyword)

    return render_template(
        "customers.html",
        customers=customer_list,
        search=keyword
    )


# ==========================================
# Freeze Customer
# ==========================================

def freeze_customer_controller(customer_id):

    try:

        freeze_customer(customer_id)

        flash("Customer account frozen.", "warning")

    except Exception as e:

        flash(f"Error: {e}", "danger")

    return redirect(url_for("customer.customers"))


# ==========================================
# Activate Customer
# ==========================================

def activate_customer_controller(customer_id):

    try:

        activate_customer(customer_id)

        flash("Customer account activated.", "success")

    except Exception as e:

        flash(f"Error: {e}", "danger")

    return redirect(url_for("customer.customers"))


# ==========================================
# Soft Delete Customer
# ==========================================

def delete_customer_controller(customer_id):

    try:

        delete_customer(customer_id)

        flash("Customer deleted successfully.", "info")

    except Exception as e:

        flash(f"Error: {e}", "danger")

    return redirect(url_for("customer.customers"))