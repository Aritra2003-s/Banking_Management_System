# 🏦 Banking Management System

A secure and modern **Banking Management System** built with **Python** and **Flask**. This project demonstrates object-oriented programming, authentication, transaction management, database integration, and reporting features in a real-world banking application.

---

## 📌 Features

### 🔐 Authentication
- Customer Registration
- Secure Login & Logout
- Password Hashing
- Session Management
- Role-Based Access (Admin & Customer)

### 👤 Customer Management
- Create New Customer
- View Customer Profile
- Update Profile Information
- Search Customers
- Delete Customer (Admin)

### 💳 Banking Operations
- Create Bank Account
- Deposit Money
- Withdraw Money
- Transfer Money
- Balance Enquiry

### 📜 Transaction Management
- Transaction History
- Mini Statement
- Account Statements
- Transaction Logs

### 📊 Reports
- Generate PDF Reports
- Export Transactions to Excel
- Export Accounts to CSV

### 🛡 Security
- Password Hashing
- Input Validation
- SQL Injection Protection
- Secure Sessions
- Authentication Middleware

---

# 🛠 Tech Stack

### Backend
- Python 3.x
- Flask

### Database
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

### Libraries
- Flask
- Werkzeug
- ReportLab
- OpenPyXL
- Pandas

---

# 📂 Project Structure

```
Banking_Management_System/
│
├── app.py
├── requirements.txt
├── config.py
├── README.md
│
├── database/
│   ├── banking.db
│   └── database.py
│
├── controllers/
│   ├── auth_controller.py
│   ├── customer_controller.py
│   ├── account_controller.py
│   └── transaction_controller.py
│
├── models/
│   ├── customer.py
│   ├── account.py
│   ├── transaction.py
│   └── admin.py
│
├── services/
│   ├── auth_service.py
│   ├── customer_service.py
│   ├── banking_service.py
│   └── report_service.py
│
├── routes/
│   ├── auth_routes.py
│   ├── customer_routes.py
│   ├── account_routes.py
│   └── admin_routes.py
│
├── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── utils/
    ├── helpers.py
    ├── validators.py
    └── security.py
```

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/Aritra2003-s/Banking_Management_System.git
```

## 2. Go to Project Folder

```bash
cd Banking_Management_System
```

## 3. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run the Project

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# 📈 Future Enhancements

- Email Notifications
- SMS Alerts
- OTP Verification
- Two-Factor Authentication (2FA)
- QR Code Payments
- Mobile Banking Interface
- REST API
- Docker Support
- MySQL/PostgreSQL Support
- Cloud Deployment (Render/AWS/Azure)

---

# 📷 Screenshots

Add screenshots of:

- Login Page
- Registration Page
- Admin Dashboard
- Customer Dashboard
- Deposit Page
- Withdraw Page
- Transfer Money Page
- Transaction History
- Reports

---

# 🧪 Testing

Run the application and test the following workflows:

- Register a new customer
- Login securely
- Deposit money
- Withdraw money
- Transfer funds
- View transaction history
- Generate reports

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Aritra Sarkar**

- GitHub: https://github.com/Aritra2003-s

---

⭐ If you found this project useful, don't forget to **star the repository**!