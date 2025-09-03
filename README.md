# Sistema de Microservicios con Docker y Consul

## Descripción
Sistema distribuido compuesto por microservicios para gestión de usuarios, productos y órdenes de compra, con descubrimiento de servicios mediante Consul.

## Estructura del Proyecto
microWebApp/
├── consul/
│ └── config.json
├── frontend/
│ ├── templates/
│ │ └── index.html
│ ├── config.py
│ ├── Dockerfile
│ ├── requirements.txt
│ └── run.py
├── microOrders/
│ └── orders/
│ ├── templates/
│ │ └── orders.html
│ ├── controllers/
│ │ └── order_controller.py
│ ├── models/
│ │ └── order_model.py
│ ├── config.py
│ ├── db.py
│ ├── Dockerfile
│ ├── requirements.txt
│ └── run.py
├── microProducts/
│ └── products/
│ ├── templates/
│ │ └── products.html
│ ├── controllers/
│ │ └── product_controller.py
│ ├── models/
│ │ └── product_model.py
│ ├── config.py
│ ├── db.py
│ ├── Dockerfile
│ ├── requirements.txt
│ └── run.py
├── microUsers/
│ └── users/
│ ├── templates/
│ │ └── users.html
│ ├── controllers/
│ │ └── user_controller.py
│ ├── models/
│ │ └── user_model.py
│ ├── config.py
│ ├── db.py
│ ├── Dockerfile
│ ├── requirements.txt
│ └── run.py
├── nginx/
│ └── nginx.conf
├── docker-compose.yml
├── .gitignore
├── README.md
└── Vagrantfile



## Servicios
- **Frontend**: Dashboard principal - Puerto 5000
- **Users Service**: Gestión de usuarios - Puerto 5001
- **Products Service**: Gestión de productos - Puerto 5002  
- **Orders Service**: Gestión de órdenes - Puerto 5003
- **Consul**: Service discovery - Puerto 8500
- **Nginx**: Reverse proxy - Puerto 80

## URLs de Acceso
- **Dashboard**: http://192.168.56.10/
- **Consul UI**: http://192.168.56.10:8500
- **Usuarios**: http://192.168.56.10/users
- **Productos**: http://192.168.56.10/products
- **Órdenes**: http://192.168.56.10/orders

## Instalación y Uso

### Prerrequisitos
- Vagrant
- VirtualBox
- Docker
- Docker Compose

### Ejecución
```bash
# Iniciar VM con Vagrant
vagrant up
vagrant ssh

# Ejecutar con Docker Compose
cd /vagrant
docker-compose up -d

# Verificar servicios
docker-compose ps

Tecnologías
Flask (Python)

Docker & Docker Compose

Consul (Service Discovery)

Nginx (Reverse Proxy)

SQLite (Database)

Bootstrap 5 (Frontend)


## 4. Crear repositorio en GitHub

Ve a [github.com](https://github.com) y:
1. Haz clic en "New repository"
2. Nombre: `microWebAppParcial` (o el nombre que prefieras)
3. Descripción: "Sistema de microservicios con Docker y Consul"
4. **NO inicialices con README** (ya tenemos uno)
5. Haz clic en "Create repository"

## 5. Subir código a GitHub

```bash
# Agregar el remote de GitHub
git remote add origin https://github.com/tu_usuario/microWebAppParcial.git

# Cambiar a rama main
git branch -M main

# Hacer push
git push -u origin main
# microwebParcial
# microwebParcial
