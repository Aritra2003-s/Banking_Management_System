from flask import Flask, render_template
from flask_login import LoginManager, login_required

# Blueprint Imports
from routes.auth_routes import auth_bp
from routes.customer_routes import customer_bp
from routes.account_routes import account_bp
from routes.report_routes import report_bp

# Model and Database Imports
from models.customer import Customer
from database.database import get_db_connection


# ==========================================
# Create Flask Application
# ==========================================

app = Flask(__name__)

# Secret Key (Move to .env in production)
app.secret_key = "bank_secret_key"


# ==========================================
# Flask-Login Configuration
# ==========================================

login_manager = LoginManager()
login_manager.init_app(app)

# Redirect unauthenticated users to login page
login_manager.login_view = "auth.login_page"
login_manager.login_message = "Please login to continue."
login_manager.login_message_category = "warning"


# ==========================================
# User Loader
# ==========================================

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            SELECT *
            FROM Customer
            WHERE customer_id = ?
            """,
            (user_id,)
        )
        user = cursor.fetchone()
        if user:
            return Customer(user)
        return None
    finally:
        cursor.close()
        conn.close()


# ==========================================
# Register Blueprints
# ==========================================

app.register_blueprint(auth_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(account_bp)
app.register_blueprint(report_bp)


# ==========================================
# Protected Routes
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/accounts")
@login_required
def accounts():
    return render_template("accounts.html")


@app.route("/transactions")
@login_required
def transactions():
    return render_template("transactions.html")


# ==========================================
# Home Page
# ==========================================

@app.route("/")
def home():
    return render_template("login.html")


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)