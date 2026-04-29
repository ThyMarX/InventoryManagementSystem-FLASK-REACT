from flask import Blueprint, jsonify, request
from services.product_service import ProductService

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    # """
    # Hent alle produkter
    # ---
    # responses:
    #   200:
    #     description: En liste over alle produkter i systemet
    # """
    products = ProductService.get_all_products()
    # Konverterer SQLAlchemy objekter til JSON-venlige lister
    output = []
    for p in products:
        output.append({"id": p.id, "name": p.name, "price": p.price})
    if not products:
        return jsonify({"message": "Ingen produkter fundet"}), 404
    return jsonify(output)

@product_bp.route('/warehouses/<int:warehouse_id>/products', methods=['GET'])
def get_warehouse_products(warehouse_id):
    products = ProductService.get_products_by_warehouse(warehouse_id)
    if not products:
        return jsonify({"message": "Ingen produkter fundet på dette lager"}), 404
    return jsonify(products)

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Manglende navn eller pris"}), 400
    
    product = ProductService.create_product(data)
    return jsonify({"message": "Produkt oprettet og tilføjet til alle lagre", "id": product.id}), 201

@product_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = ProductService.update_product(id, data)
    if not product:
        return jsonify({"error": "Produkt ikke fundet"}), 404
    return jsonify({"message": "Produkt opdateret"})

@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    success = ProductService.delete_product(id)
    if not success:
        return jsonify({"error": "Produkt ikke fundet"}), 404
    return jsonify({"message": "Produkt slettet"})