# Inputs the database with some basic data

from app import create_app
from models import db, User, Product, Warehouse, ProductsInWarehouse

app = create_app()

with app.app_context():
    # 1. Opret en test-bruger
    admin = User(name="Admin", username="admin", password="123", type="admin")
    db.session.add(admin)
    db.session.commit()

    # 2. Opret et lager
    wh1 = Warehouse(name="Hovedlageret", location="København", site_manager_id=admin.id)
    db.session.add(wh1)
    db.session.commit()

    # 3. Opret et produkt
    laptop = Product(name="MacBook Pro", price=15000, author_id=admin.id)
    db.session.add(laptop)
    db.session.commit()

    # 4. Læg produktet på lageret
    stock = ProductsInWarehouse(product_id=laptop.id, warehouse_id=wh1.id, quantity=10)
    db.session.add(stock)
    db.session.commit()

    print("Test-data er nu indsat!")
