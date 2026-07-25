from flask import Blueprint

from controllers.customer_controller import (
    customers,
    add_customer_page,
    add_customer_controller,
    edit_customer_page,
    update_customer_controller,
    search_customer,
    freeze_customer_controller,
    activate_customer_controller,
    delete_customer_controller
)

# ==========================================
# Customer Blueprint
# ==========================================

customer_bp = Blueprint(
    "customer",
    __name__,
    url_prefix="/customers"
)


# ==========================================
# View All Customers
# URL:
# GET /customers
# ==========================================

@customer_bp.route("/")
def customers_route():

    return customers()


# ==========================================
# Add Customer Page
# URL:
# GET /customers/add
# ==========================================

@customer_bp.route("/add")
def add_customer():

    return add_customer_page()


# ==========================================
# Save New Customer
# URL:
# POST /customers/add
# ==========================================

@customer_bp.route("/add", methods=["POST"])
def save_customer():

    return add_customer_controller()


# ==========================================
# Edit Customer Page
# URL:
# GET /customers/edit/<customer_id>
# ==========================================

@customer_bp.route("/edit/<int:customer_id>")
def edit_customer(customer_id):

    return edit_customer_page(customer_id)


# ==========================================
# Update Customer
# URL:
# POST /customers/edit/<customer_id>
# ==========================================

@customer_bp.route("/edit/<int:customer_id>", methods=["POST"])
def update_customer(customer_id):

    return update_customer_controller(customer_id)


# ==========================================
# Search Customer
# URL:
# GET /customers/search
# Example:
# /customers/search?search=Rahul
# ==========================================

@customer_bp.route("/search")
def search():

    return search_customer()


# ==========================================
# Freeze Customer
# URL:
# GET /customers/freeze/<customer_id>
# ==========================================

@customer_bp.route("/freeze/<int:customer_id>")
def freeze_customer(customer_id):

    return freeze_customer_controller(customer_id)


# ==========================================
# Activate Customer
# URL:
# GET /customers/activate/<customer_id>
# ==========================================

@customer_bp.route("/activate/<int:customer_id>")
def activate_customer(customer_id):

    return activate_customer_controller(customer_id)


# ==========================================
# Soft Delete Customer
# URL:
# GET /customers/delete/<customer_id>
# ==========================================

@customer_bp.route("/delete/<int:customer_id>")
def delete_customer(customer_id):

    return delete_customer_controller(customer_id)