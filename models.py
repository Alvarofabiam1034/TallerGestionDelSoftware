from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Modelo de Usuario con roles diferenciados"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Admin, Mesero, Cliente
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Genera hash de contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username} - {self.role}>'

class MenuItem(db.Model):
    """Modelo de ítems del menú"""
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MenuItem {self.nombre}>'

class Pedido(db.Model):
    """Modelo de pedidos"""
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    mesa = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), default='Pendiente')  # Pendiente, En preparación, Servido
    mesero_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    mesero = db.relationship('User', backref='pedidos')
    items = db.relationship('PedidoItem', back_populates='pedido', cascade='all, delete-orphan')
    
    def calcular_total(self):
        """Calcula el total del pedido"""
        return sum(item.precio_unitario * item.cantidad for item in self.items)
    
    def __repr__(self):
        return f'<Pedido {self.id} - Mesa {self.mesa} - {self.estado}>'

class PedidoItem(db.Model):
    """Modelo de ítems dentro de un pedido"""
    __tablename__ = 'pedido_items'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)
    
    pedido = db.relationship('Pedido', back_populates='items')
    menu_item = db.relationship('MenuItem')
    
    def __repr__(self):
        return f'<PedidoItem {self.cantidad}x {self.menu_item.nombre if self.menu_item else ""}>'

class Reserva(db.Model):
    """Modelo de reservas"""
    __tablename__ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    cliente = db.relationship('User', backref='reservas')
    
    def __repr__(self):
        return f'<Reserva {self.nombre_cliente} - {self.fecha} {self.hora}>'

