# MotoGama Elite — Sistema de Gestión de Concesionario

Aplicación web desarrollada con **Python + Flask + SQLite** para la gestión de un concesionario de motocicletas de alta gama.

## Requisitos

- Python 3.10+
- pip

## Instalación y Ejecución

```bash
# 1. Clonar o descomprimir el proyecto
cd concesionario

# 2. (Opcional) Crear entorno virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: **http://127.0.0.1:5000**

> La base de datos SQLite se crea automáticamente en `database/concesionario.db` con datos de ejemplo al primer inicio.

## Módulos

| Módulo | Ruta | Descripción |
|---|---|---|
| Dashboard | `/` | Estadísticas generales |
| Inventario | `/vehiculos` | CRUD de motocicletas con filtros |
| Clientes | `/clientes` | CRUD de clientes con búsqueda |
| Ventas | `/ventas` | Registro y listado de ventas |
| Reportes | `/reportes` | Análisis de ingresos e inventario |
| API REST | `/api/vehiculo/<id>` | Datos de vehículo en JSON |

## Estructura del Proyecto

```
concesionario/
├── app.py                  # Aplicación Flask principal
├── requirements.txt
├── database/
│   ├── schema.sql          # Esquema + datos de ejemplo
│   └── concesionario.db    # Base de datos SQLite (auto-generada)
├── static/
│   ├── css/style.css       # Estilos (rojo/negro/blanco)
│   └── js/main.js          # JavaScript
└── templates/
    ├── base.html
    ├── index.html
    ├── vehiculos.html
    ├── vehiculo_form.html
    ├── clientes.html
    ├── cliente_form.html
    ├── ventas.html
    ├── venta_form.html
    └── reportes.html
```

## Tecnologías

- **Backend:** Python 3 + Flask
- **Base de datos:** SQLite (schema.sql exportable)
- **Frontend:** HTML5, CSS3 (custom), JavaScript vanilla
- **Arquitectura:** MVC · API REST básica
- **Fuentes:** Bebas Neue, Rajdhani, Inter (Google Fonts)

---
*Proyecto ADSO18 — Evaluación Desarrollo de Software*
