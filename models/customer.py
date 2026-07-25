from flask_login import UserMixin

class Customer(UserMixin):

    def __init__(self, customer):
        self.id = customer["customer_id"]
        self.first_name = customer["first_name"]
        self.last_name = customer["last_name"]
        self.email = customer["email"]
        self.phone = customer["phone"]