from flask import Flask, jsonify
from db import db
from config import Config
import consul
import os

# Importar el controlador directamente
from users.controller.user_controller import user_controller

def register_service():
    try:
        c = consul.Consul(host='consul', port=8500)
        service_id = f"users-service-{os.getenv('HOSTNAME', 'localhost')}"
        c.agent.service.register(
            'users-service',
            service_id=service_id,
            address='micro-users',
            port=5000,
            check=consul.Check.http(
                f'http://micro-users:5000/health',
                interval='10s'
            )
        )
        print("Servicio registrado en Consul exitosamente")
    except Exception as e:
        print(f"Error registrando servicio en Consul: {e}")

def create_app():
    app = Flask(__name__, template_folder='users/templates')
    app.config.from_object(Config)
    
    db.init_app(app)
    app.register_blueprint(user_controller)
    
    with app.app_context():
        db.create_all()
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    register_service()
    app.run(host='0.0.0.0', port=5000, debug=True)
