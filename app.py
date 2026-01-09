from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, MenuItem, Pedido, PedidoItem, Reserva
from datetime import datetime, date, time
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurante.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def init_db():
    """Inicializa la base de datos y crea usuario admin por defecto"""
    with app.app_context():
        db.create_all()
        
        # Crear usuario admin por defecto si no existe
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@restaurante.com', role='Admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Usuario admin creado: username='admin', password='admin123'")

# Middleware para verificar autenticación
@app.before_request
def require_login():
    """Verifica que el usuario esté autenticado excepto en rutas públicas"""
    allowed_routes = ['login', 'register', 'static', 'menu_publico']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

# ==================== AUTENTICACIÓN ====================

@app.route('/')
def index():
    """Redirige al dashboard según el rol del usuario"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if user.role == 'Admin':
        return redirect(url_for('admin_dashboard'))
    elif user.role == 'Mesero':
        return redirect(url_for('mesero_dashboard'))
    elif user.role == 'Cliente':
        return redirect(url_for('cliente_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'Cliente')
        
        if User.query.filter_by(username=username).first():
            flash('El usuario ya existe', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registro exitoso. Puedes iniciar sesión ahora.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

# ==================== DASHBOARDS POR ROL ====================

@app.route('/admin')
def admin_dashboard():
    """Dashboard del administrador"""
    if session.get('role') != 'Admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    total_pedidos = Pedido.query.count()
    pedidos_pendientes = Pedido.query.filter_by(estado='Pendiente').count()
    total_reservas = Reserva.query.filter(Reserva.fecha >= date.today()).count()
    
    return render_template('admin/dashboard.html', 
                         total_pedidos=total_pedidos,
                         pedidos_pendientes=pedidos_pendientes,
                         total_reservas=total_reservas)

@app.route('/mesero')
def mesero_dashboard():
    """Dashboard del mesero"""
    if session.get('role') != 'Mesero':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    pedidos_activos = Pedido.query.filter(Pedido.estado != 'Servido').all()
    return render_template('mesero/dashboard.html', pedidos_activos=pedidos_activos)

@app.route('/cliente')
def cliente_dashboard():
    """Dashboard del cliente"""
    if session.get('role') != 'Cliente':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    return render_template('cliente/dashboard.html')

# ==================== MÓDULO DE MENÚ ====================

@app.route('/admin/menu')
def admin_menu():
    """Gestión de menú para admin (CRUD)"""
    if session.get('role') != 'Admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    items = MenuItem.query.all()
    return render_template('admin/menu.html', items=items)

@app.route('/admin/menu/nuevo', methods=['GET', 'POST'])
def admin_menu_nuevo():
    """Crear nuevo ítem de menú"""
    if session.get('role') != 'Admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        item = MenuItem(
            nombre=request.form.get('nombre'),
            descripcion=request.form.get('descripcion'),
            precio=float(request.form.get('precio')),
            categoria=request.form.get('categoria')
        )
        db.session.add(item)
        db.session.commit()
        flash('Ítem agregado al menú', 'success')
        return redirect(url_for('admin_menu'))
    
    return render_template('admin/menu_form.html')

@app.route('/admin/menu/editar/<int:id>', methods=['GET', 'POST'])
def admin_menu_editar(id):
    """Editar ítem de menú"""
    if session.get('role') != 'Admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    item = MenuItem.query.get_or_404(id)
    
    if request.method == 'POST':
        item.nombre = request.form.get('nombre')
        item.descripcion = request.form.get('descripcion')
        item.precio = float(request.form.get('precio'))
        item.categoria = request.form.get('categoria')
        db.session.commit()
        flash('Ítem actualizado', 'success')
        return redirect(url_for('admin_menu'))
    
    return render_template('admin/menu_form.html', item=item)

@app.route('/admin/menu/eliminar/<int:id>', methods=['POST'])
def admin_menu_eliminar(id):
    """Eliminar ítem de menú"""
    if session.get('role') != 'Admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    item = MenuItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Ítem eliminado', 'success')
    return redirect(url_for('admin_menu'))

@app.route('/menu')
def menu_publico():
    """Vista pública del menú para clientes"""
    items = MenuItem.query.all()
    categorias = db.session.query(MenuItem.categoria).distinct().all()
    categorias = [c[0] for c in categorias]
    return render_template('menu_publico.html', items=items, categorias=categorias)

# ==================== MÓDULO DE PEDIDOS ====================

@app.route('/mesero/pedidos/nuevo', methods=['GET', 'POST'])
def mesero_pedido_nuevo():
    """Crear nuevo pedido"""
    if session.get('role') != 'Mesero':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        mesa = request.form.get('mesa')
        items_seleccionados = request.form.getlist('items')
        cantidades = request.form.getlist('cantidades')
        
        pedido = Pedido(mesa=mesa, mesero_id=session['user_id'], estado='Pendiente')
        db.session.add(pedido)
        db.session.flush()
        
        for item_id, cantidad in zip(items_seleccionados, cantidades):
            if int(cantidad) > 0:
                menu_item = MenuItem.query.get(item_id)
                if menu_item:
                    pedido_item = PedidoItem(
                        pedido_id=pedido.id,
                        menu_item_id=item_id,
                        cantidad=int(cantidad),
                        precio_unitario=menu_item.precio
                    )
                    db.session.add(pedido_item)
        
        db.session.commit()
        flash('Pedido creado exitosamente', 'success')
        return redirect(url_for('mesero_dashboard'))
    
    items = MenuItem.query.all()
    return render_template('mesero/pedido_nuevo.html', items=items)

@app.route('/mesero/pedidos/<int:id>')
def mesero_pedido_detalle(id):
    """Ver detalle de un pedido"""
    pedido = Pedido.query.get_or_404(id)
    return render_template('mesero/pedido_detalle.html', pedido=pedido)

@app.route('/admin/pedidos')
def admin_pedidos():
    """Lista de pedidos para admin"""
    if session.get('role') != 'Admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    pedidos = Pedido.query.order_by(Pedido.created_at.desc()).all()
    return render_template('admin/pedidos.html', pedidos=pedidos)

@app.route('/pedidos/<int:id>/cambiar_estado', methods=['POST'])
def cambiar_estado_pedido(id):
    """Cambiar estado de un pedido"""
    pedido = Pedido.query.get_or_404(id)
    
    if session.get('role') not in ['Admin', 'Mesero']:
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    nuevo_estado = request.form.get('estado')
    if nuevo_estado in ['Pendiente', 'En preparación', 'Servido']:
        pedido.estado = nuevo_estado
        pedido.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f'Estado cambiado a: {nuevo_estado}', 'success')
    
    if session.get('role') == 'Admin':
        return redirect(url_for('admin_pedidos'))
    return redirect(url_for('mesero_dashboard'))

# ==================== MÓDULO DE RESERVAS ====================

@app.route('/cliente/reservas/nueva', methods=['GET', 'POST'])
def cliente_reserva_nueva():
    """Formulario para crear nueva reserva"""
    if request.method == 'POST':
        reserva = Reserva(
            nombre_cliente=request.form.get('nombre_cliente'),
            fecha=datetime.strptime(request.form.get('fecha'), '%Y-%m-%d').date(),
            hora=datetime.strptime(request.form.get('hora'), '%H:%M').time(),
            numero_personas=int(request.form.get('numero_personas')),
            cliente_id=session.get('user_id')
        )
        db.session.add(reserva)
        db.session.commit()
        flash('Reserva realizada exitosamente', 'success')
        return redirect(url_for('cliente_dashboard'))
    
    return render_template('cliente/reserva_nueva.html')

@app.route('/admin/reservas')
def admin_reservas():
    """Lista de reservas para admin"""
    if session.get('role') != 'Admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    reservas = Reserva.query.filter(Reserva.fecha >= date.today()).order_by(Reserva.fecha, Reserva.hora).all()
    return render_template('admin/reservas.html', reservas=reservas)

# ==================== MÓDULO DE FACTURACIÓN Y REPORTES (PLACEHOLDERS) ====================

@app.route('/admin/cerrar_caja', methods=['GET', 'POST'])
def admin_cerrar_caja():
    """Cerrar caja diaria (placeholder)"""
    if session.get('role') != 'Admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        fecha = request.form.get('fecha', date.today().isoformat())
        # Aquí iría la lógica de cierre de caja
        flash(f'Caja cerrada exitosamente para la fecha: {fecha}', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/cerrar_caja.html')

@app.route('/admin/reporte_ventas')
def admin_reporte_ventas():
    """Reporte básico de ventas del día (placeholder)"""
    if session.get('role') != 'Admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))
    
    fecha = request.args.get('fecha', date.today().isoformat())
    # Aquí iría la lógica del reporte
    # Por ahora solo retornamos un mensaje
    
    pedidos_del_dia = Pedido.query.filter(
        db.func.date(Pedido.created_at) == fecha
    ).all()
    
    total_ventas = sum(pedido.calcular_total() for pedido in pedidos_del_dia)
    
    return render_template('admin/reporte_ventas.html', 
                         fecha=fecha,
                         total_pedidos=len(pedidos_del_dia),
                         total_ventas=total_ventas,
                         pedidos=pedidos_del_dia)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

