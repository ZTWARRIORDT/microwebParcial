from flask import Flask, render_template
import consul
import os

def register_service():
    try:
        c = consul.Consul(host='consul', port=8500)
        service_id = f"frontend-service-{os.getenv('HOSTNAME', 'localhost')}"
        c.agent.service.register(
            'frontend-service',
            service_id=service_id,
            address='frontend',
            port=5000,
            check=consul.Check.http(
                f'http://frontend:5000/health',
                interval='10s'
            )
        )
        print("Frontend service registered in Consul successfully")
    except Exception as e:
        print(f"Error registering frontend service in Consul: {e}")

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    register_service()
    app.run(host='0.0.0.0', port=5000, debug=True)
