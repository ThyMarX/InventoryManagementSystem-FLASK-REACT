# The structure for the different tables in the database

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. Users (Is used by almost all other tables as a Author/Manager)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50))                 # Admin, Manager, Employee, Customer
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Who created this user?

# 2. Products
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Who created this product?
    
    # Relations (is this necesarry?)
    warehouses = db.relationship('ProductsInWarehouse', backref='product', cascade="all, delete-orphan")

# 3. Warehouses
class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    site_manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# 4. ProductsInWarehouses (M-M relation between Products and Warehouses)
class ProductsInWarehouse(db.Model):
    __tablename__ = 'products_in_warehouses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)

# 5. Orders
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    current_status = db.Column(db.String(50))       # Sold, Reserved, Canceled, In_Transfer, Transferred, Refunded, Partially_Refunded
    last_changed = db.Column(db.DateTime, default=datetime.utcnow)  # When was the last time the order was changed/updated
    full_status = db.Column(db.String(1000))        # A long string showing all that has happened to the order, ex:, "RESERVED by AUTHOR1 at WAREHOUSE1 the XX/XX/XX -> SOLD by AUTHOR2 the YY/YY/YY".
    total_value = db.Column(db.Integer, default=0)  # The total price value of the entire order
    from_warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    order_note = db.Column(db.String(255))          # A string the employee may write a note in, if needed
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))    # Which user originally created the order
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=0)  # Which customer is asociated with the order, if any?
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 6. ProductsInOrders (M-M relation between Products and Orders)
class ProductsInOrder(db.Model):
    __tablename__ = 'products_in_orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    price = db.Column(db.Integer)               # The price when the order was made
    quantity = db.Column(db.Integer, default=0) # How many of the specific product was bought in the order

# 7. Operations (A log for all transactions, aka order creations and changes, along with all other changes made in the databae)
class Operation(db.Model):
    __tablename__ = 'operations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50))         # Order creation, Order change, Product creation, Product change, etc.
    foreign_key = db.Column(db.String(50))  # If it's f.ex a Order creation, then this shows that orders ID
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
