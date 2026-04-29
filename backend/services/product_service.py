# Queries to the database concerning Products

from models import Product, ProductsInWarehouse, Warehouse, db

class ProductService:
    @staticmethod
    def get_all_products():
        # Henter alle produkter
        return Product.query.all()

    @staticmethod
    def get_products_by_warehouse(warehouse_id):
        # Joiner ProductsInWarehouse med Product for at få navne og priser med
        results = db.session.query(Product, ProductsInWarehouse.quantity).\
            join(ProductsInWarehouse, Product.id == ProductsInWarehouse.product_id).\
            filter(ProductsInWarehouse.warehouse_id == warehouse_id).all()
        
        # Formaterer resultatet til en liste af ordbøger
        products = []
        for product, quantity in results:
            products.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity
            })
        return products
    
    @staticmethod
    def create_product(data):
        # 1. Opret produktet
        new_product = Product(
            name=data.get('name'),
            price=data.get('price'),
            author_id=data.get('author_id')
        )
        db.session.add(new_product)
        db.session.flush()

        # 2. Hent alle eksisterende varehuse
        all_warehouses = Warehouse.query.all()
        
        # 3. Opret en 0-beholdning for hvert varehus
        for wh in all_warehouses:
            stock = ProductsInWarehouse(
                product_id=new_product.id,
                warehouse_id=wh.id,
                quantity=0
            )
            db.session.add(stock)
        
        db.session.commit()
        return new_product

    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get(product_id)
        if not product:
            return None
        
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        # Vi opdaterer ikke author_id, da det er den oprindelige skaber
        
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False
