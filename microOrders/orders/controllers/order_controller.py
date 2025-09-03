from flask import Blueprint, request, jsonify, render_template, session
from db import db
from orders.models.order_model import Order
from config import Config
import requests
import json
import consul

order_controller = Blueprint('order_controller', __name__)

def get_service_url(service_name):
    try:
        c = consul.Consul(host='consul', port=8500)
        _, services = c.catalog.service(service_name)
        if services:
            service = services[0]
            return f"http://{service['ServiceAddress']}:{service['ServicePort']}"
    except Exception as e:
        print(f"Error obteniendo servicio {service_name} desde Consul: {e}")
    
    # Fallback a nombres de servicio de Docker
    return f"http://{service_name}"

@order_controller.route('/api/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@order_controller.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())

@order_controller.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    # Para testing, simular sesión de usuario
    session['user_id'] = session.get('user_id', 1)
    session['username'] = session.get('username', 'testuser')
    session['email'] = session.get('email', 'test@example.com')
    
    if 'user_id' not in session:
        return jsonify({'message': 'Usuario no autenticado'}), 401
    
    user_id = session['user_id']
    user_name = session.get('username', '')
    user_email = session.get('email', '')
    
    products = data.get('products')
    if not products or not isinstance(products, list):
        return jsonify({'message': 'Falta o es inválida la información de los productos'}), 400
    
    # Calcular total y verificar stock
    total = 0
    products_service_url = get_service_url('products-service')
    order_items = []  # Lista para almacenar información completa de productos
    
    for product in products:
        product_id = product['product_id']
        quantity = product['quantity']
        
        # Obtener información completa del producto
        try:
            response = requests.get(f"{products_service_url}/api/products/{product_id}")
            if response.status_code == 200:
                product_data = response.json()
                product_total = product_data['price'] * quantity
                total += product_total
                
                # Guardar información completa del producto
                order_item = {
                    'product_id': product_id,
                    'name': product_data['name'],
                    'price': product_data['price'],
                    'quantity': quantity,
                    'subtotal': product_total
                }
                order_items.append(order_item)
                
                # Verificar stock
                if product_data['stock'] < quantity:
                    return jsonify({'message': f'Stock insuficiente para el producto {product_data["name"]}'}), 400
            else:
                return jsonify({'message': f'Producto {product_id} no encontrado'}), 404
        except Exception as e:
            print(f"Error conectando con servicio de productos: {e}")
            return jsonify({'message': 'Error al conectar con el servicio de productos'}), 500
    
    # Actualizar stock
    for item in order_items:
        try:
            update_data = {
                'product_id': item['product_id'],
                'quantity': item['quantity']
            }
            response = requests.post(
                f"{products_service_url}/api/products/update-stock",
                json=update_data
            )
            if response.status_code != 200:
                return jsonify({'message': 'Error al actualizar stock'}), 500
        except Exception as e:
            print(f"Error actualizando stock: {e}")
            return jsonify({'message': 'Error al conectar con el servicio de productos'}), 500
    
    # Crear orden con información completa de productos
    order = Order(
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        total=total,
        items=json.dumps(order_items)  # Guardar información completa
    )
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify({
        'message': 'Orden creada exitosamente', 
        'order_id': order.id,
        'total': total
    }), 201

@order_controller.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    # Aquí puedes implementar la lógica de actualización según tus necesidades
    return jsonify({'message': 'Orden actualizada exitosamente'})

@order_controller.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Orden eliminada exitosamente'})

@order_controller.route('/orders')
def orders_page():
    return render_template('orders.html')

# Ruta principal redirige a orders
@order_controller.route('/')
def index():
    return render_template('orders.html')
