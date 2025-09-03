from flask import Blueprint, request, jsonify, render_template
from db import db
from products.models.product_model import Product

product_controller = Blueprint('product_controller', __name__)

@product_controller.route('/api/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@product_controller.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@product_controller.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data['stock']
    )
    
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Producto creado exitosamente'}), 201

@product_controller.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']
    
    db.session.commit()
    return jsonify({'message': 'Producto actualizado exitosamente'})

@product_controller.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Producto eliminado exitosamente'})

@product_controller.route('/api/products/update-stock', methods=['POST'])
def update_stock():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']
    
    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        return jsonify({'message': 'Stock insuficiente'}), 400
    
    product.stock -= quantity
    db.session.commit()
    return jsonify({'message': 'Stock actualizado exitosamente'})

@product_controller.route('/products')
def products_page():
    return render_template('products.html')

# Ruta principal redirige a products
@product_controller.route('/')
def index():
    return render_template('products.html')
