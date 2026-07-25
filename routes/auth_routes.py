from flask import Blueprint
from flask import render_template

from controllers.auth_controller import (
    register,
    login,
    logout
)

# ==========================================
# Authentication Blueprint
# ==========================================

auth_bp = Blueprint("auth", __name__)

# ==========================================
# Registration Routes
# ==========================================

@auth_bp.route("/register", methods=["GET"])
def register_page():

    return render_template("register.html")


@auth_bp.route("/register", methods=["POST"])
def register_user_route():

    return register()


# ==========================================
# Login Routes
# ==========================================

@auth_bp.route("/login", methods=["GET"])
def login_page():

    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_user_route():

    return login()


# ==========================================
# Logout Route
# ==========================================

@auth_bp.route("/logout", methods=["GET"])
def logout_route():

    return logout()