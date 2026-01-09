# # SIGR - Sistema Integral de Gestión de Restaurante

Sistema básico de gestión para restaurantes que incluye módulos de autenticación, menú digital, pedidos, reservas y reportes básicos.

## 🚀 Características

### Módulos Implementados

1. **Autenticación y Gestión de Usuarios**
   - Sistema de registro y login
   - Tres roles diferenciados: Admin, Mesero, Cliente
   - Gestión de sesiones

2. **Menú Digital**
   - CRUD completo de ítems del menú para administradores
   - Vista pública del menú para clientes
   - Categorización de platos (Entrada, Plato Principal, Postre, Bebida, Acompañamiento)

3. **Gestión de Pedidos**
   - Creación de pedidos por meseros
   - Asignación de pedidos a mesas
   - Estados: Pendiente, En preparación, Servido
   - Visualización de pedidos activos
   - Cambio de estado de pedidos

4. **Reservas**
   - Formulario para que clientes realicen reservas
   - Visualización de reservas para administradores
   - Filtrado por fecha

5. **Facturación y Reportes (Placeholder)**
   - Endpoint para cerrar caja diaria (placeholder)
   - Reporte básico de ventas del día (con funcionalidad mínima)

## 🛠️ Tecnologías

- **Backend:** Python 3.x + Flask
- **Base de Datos:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML5 + TailwindCSS (via CDN)
- **Autenticación:** Werkzeug Security

## 📋 Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. **Clonar o descargar el proyecto**

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Inicializar la base de datos**
   Al ejecutar la aplicación por primera vez, la base de datos se creará automáticamente con un usuario administrador por defecto.

## 🚀 Ejecución

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 👤 Usuario por Defecto

Al inicializar la aplicación, se crea automáticamente un usuario administrador:

- **Usuario:** `admin`
- **Contraseña:** `admin123`

**⚠️ IMPORTANTE:** Cambia la contraseña del administrador en producción y actualiza la `SECRET_KEY` en `app.py`.

## 📁 Estructura del Proyecto

```
.
├── app.py                  # Aplicación principal Flask
├── models.py               # Modelos de base de datos (SQLAlchemy)
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
├── restaurante.db         # Base de datos SQLite (se crea automáticamente)
├── templates/             # Plantillas HTML
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── menu_publico.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── menu.html
│   │   ├── menu_form.html
│   │   ├── pedidos.html
│   │   ├── reservas.html
│   │   ├── cerrar_caja.html
│   │   └── reporte_ventas.html
│   ├── mesero/
│   │   ├── dashboard.html
│   │   ├── pedido_nuevo.html
│   │   └── pedido_detalle.html
│   └── cliente/
│       ├── dashboard.html
│       └── reserva_nueva.html
└── static/                # Archivos estáticos (CSS, JS, imágenes)
```

## 🔐 Roles y Permisos

### Administrador (Admin)
- Acceso completo al sistema
- Gestión de menú (CRUD)
- Visualización de todos los pedidos
- Visualización de reservas
- Acceso a reportes y cierre de caja

### Mesero
- Crear y gestionar pedidos
- Cambiar estado de pedidos
- Ver menú
- Ver pedidos activos

### Cliente
- Ver menú público
- Realizar reservas
- Acceso limitado al sistema

## 📝 Notas de Desarrollo

### Base de Datos
- La base de datos SQLite se crea automáticamente al ejecutar la aplicación por primera vez
- El esquema se define en `models.py` usando SQLAlchemy
- El archivo `restaurante.db` se genera en el directorio raíz del proyecto

### Seguridad
- Las contraseñas se almacenan usando hash (Werkzeug Security)
- La `SECRET_KEY` actual es solo para desarrollo. **Debe cambiarse en producción**
- Las sesiones están protegidas por middleware de autenticación

### Funcionalidades Placeholder
- **Cerrar Caja:** Actualmente solo muestra un mensaje de éxito. En producción, debería calcular totales, generar reportes, etc.
- **Reporte de Ventas:** Muestra un reporte básico con totales del día. En producción, debería incluir gráficos, comparativas, exportación, etc.

## 🔄 Próximos Pasos (Sugerencias)

Para expandir esta línea base, considera:

1. **Mejoras de Seguridad:**
   - Implementar CSRF protection
   - Agregar rate limiting
   - Mejorar validación de formularios

2. **Funcionalidades Adicionales:**
   - Sistema de facturación completo
   - Gráficos y estadísticas avanzadas
   - Notificaciones en tiempo real
   - Integración con sistemas de pago
   - App móvil

3. **Mejoras de UX/UI:**
   - Diseño más moderno y responsive
   - Búsqueda y filtros avanzados
   - Drag & drop para reorganizar pedidos
   - Vista previa de menú mejorada

4. **Optimizaciones:**
   - Caché de consultas frecuentes
   - Paginación de resultados
   - Optimización de base de datos
   - Migración a PostgreSQL para producción

## 🐛 Solución de Problemas

**Error: "No module named 'flask_sqlalchemy'"**
- Asegúrate de haber instalado las dependencias: `pip install -r requirements.txt`

**Error: "Database is locked"**
- Cierra todas las conexiones a la base de datos y vuelve a intentar
- En desarrollo, reinicia el servidor Flask

**La base de datos no se crea**
- Verifica que tienes permisos de escritura en el directorio del proyecto
- Revisa los logs de Flask para ver errores específicos

## 📄 Licencia

Este proyecto es una línea base para desarrollo. Úsalo como punto de partida para tu propio sistema.

## 👥 Contribución

Este es un esqueleto base. Siéntete libre de expandirlo y adaptarlo a tus necesidades.

---

**Versión:** 1.0.0 (Línea Base)
**Fecha:** 2024

