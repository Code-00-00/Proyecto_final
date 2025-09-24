# models.py - COMPLETO CON TODAS LAS TABLAS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ====================================================
# TABLAS PRINCIPALES YA CREADAS
# ====================================================

# Tabla de Usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_sesion = db.Column(db.DateTime)
    estado = db.Column(db.Enum('activo', 'inactivo', 'suspendido'), default='activo')
    rol = db.Column(db.Enum('usuario', 'administrador', 'restaurante'), default='usuario')
    verificado = db.Column(db.Boolean, default=False)
    genero = db.Column(db.Enum('masculino', 'femenino', 'otro', 'no_especifica'))
    fecha_nacimiento = db.Column(db.Date)
    foto_perfil = db.Column(db.String(500))
    
    # Relaciones
    favoritos = db.relationship('Favorito', backref='usuario', lazy=True, cascade='all, delete-orphan')
    reservas = db.relationship('Reserva', backref='usuario', lazy=True, cascade='all, delete-orphan')
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True, cascade='all, delete-orphan')
    reseñas = db.relationship('Reseña', backref='usuario', lazy=True, cascade='all, delete-orphan')
    direcciones = db.relationship('DireccionUsuario', backref='usuario', lazy=True, cascade='all, delete-orphan')
    metodos_pago = db.relationship('MetodoPago', backref='usuario', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Tabla de Restaurantes
class Restaurante(db.Model):
    __tablename__ = 'restaurantes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    descripcion = db.Column(db.Text)
    tipo_cocina = db.Column(db.String(100))
    rating = db.Column(db.Numeric(2,1), default=0.0)
    numero_reviews = db.Column(db.Integer, default=0)
    distancia = db.Column(db.String(20))
    precio_rango = db.Column(db.String(10))
    direccion = db.Column(db.Text)
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    latitud = db.Column(db.Numeric(10, 8))
    longitud = db.Column(db.Numeric(11, 8))
    telefono = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    email = db.Column(db.String(255))
    sitio_web = db.Column(db.String(255))
    horario_apertura = db.Column(db.Time)
    horario_cierre = db.Column(db.Time)
    dias_abierto = db.Column(db.String(50))
    delivery = db.Column(db.Boolean, default=False)
    pickup = db.Column(db.Boolean, default=False)
    dine_in = db.Column(db.Boolean, default=False)
    servicio_domicilio = db.Column(db.Boolean, default=False)
    wifi_disponible = db.Column(db.Boolean, default=False)
    estacionamiento = db.Column(db.Boolean, default=False)
    aire_acondicionado = db.Column(db.Boolean, default=False)
    apto_discapacitados = db.Column(db.Boolean, default=False)
    zona_infantil = db.Column(db.Boolean, default=False)
    imagen_portada = db.Column(db.String(500))
    logo_restaurante = db.Column(db.String(500))
    estado = db.Column(db.Enum('activo', 'inactivo', 'pendiente'), default='pendiente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    favoritos = db.relationship('Favorito', backref='restaurante', lazy=True, cascade='all, delete-orphan')
    reservas = db.relationship('Reserva', backref='restaurante', lazy=True, cascade='all, delete-orphan')
    pedidos = db.relationship('Pedido', backref='restaurante', lazy=True, cascade='all, delete-orphan')
    reseñas = db.relationship('Reseña', backref='restaurante', lazy=True, cascade='all, delete-orphan')
    categorias_menu = db.relationship('CategoriaMenu', backref='restaurante', lazy=True, cascade='all, delete-orphan')
    menu_items = db.relationship('MenuItem', backref='restaurante', lazy=True, cascade='all, delete-orphan')
    horarios = db.relationship('HorarioRestaurante', backref='restaurante', lazy=True, cascade='all, delete-orphan')

# Tabla de Favoritos
class Favorito(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Índice único para evitar duplicados
    __table_args__ = (db.UniqueConstraint('usuario_id', 'restaurante_id', name='unique_favorito'),)

# Tabla de Reservas
class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False)
    nombre_reserva = db.Column(db.String(200))
    email_reserva = db.Column(db.String(255))
    telefono_reserva = db.Column(db.String(20))
    notas_especiales = db.Column(db.Text)
    codigo_reserva = db.Column(db.String(20), unique=True)
    estado = db.Column(db.Enum('pendiente', 'confirmada', 'cancelada', 'completada', 'no_asistio'), default='pendiente')
    metodo_pago = db.Column(db.Enum('efectivo', 'tarjeta', 'transferencia', 'paypal'), default='efectivo')
    deposito_pagado = db.Column(db.Numeric(10,2), default=0.00)
    total_reserva = db.Column(db.Numeric(10,2), default=0.00)
    duracion_estimada = db.Column(db.Integer)  # minutos
    mesa_asignada = db.Column(db.String(50))
    zona_mesa = db.Column(db.Enum('terraza', 'interior', 'vip', 'privada'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_cancelacion = db.Column(db.DateTime)
    motivo_cancelacion = db.Column(db.Text)

# Tabla de Pedidos
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    codigo_pedido = db.Column(db.String(20), unique=True)
    subtotal = db.Column(db.Numeric(10,2), nullable=False)
    impuestos = db.Column(db.Numeric(10,2), default=0.00)
    costo_envio = db.Column(db.Numeric(10,2), default=0.00)
    descuento = db.Column(db.Numeric(10,2), default=0.00)
    total = db.Column(db.Numeric(10,2), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'preparando', 'enviado', 'entregado', 'cancelado', 'rechazado'), default='pendiente')
    metodo_pago = db.Column(db.Enum('efectivo', 'tarjeta', 'transferencia', 'paypal', 'mercado_pago'), nullable=False)
    direccion_entrega = db.Column(db.Text)
    coordenadas_entrega = db.Column(db.Text)  # Puedes usar Point si necesitas GIS
    instrucciones_entrega = db.Column(db.Text)
    telefono_contacto = db.Column(db.String(20))
    nombre_receptor = db.Column(db.String(200))
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_preparacion = db.Column(db.DateTime)
    fecha_envio = db.Column(db.DateTime)
    fecha_entrega = db.Column(db.DateTime)
    tiempo_estimado_entrega = db.Column(db.Integer)  # minutos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    items = db.relationship('PedidoItem', backref='pedido', lazy=True, cascade='all, delete-orphan')

class PedidoItem(db.Model):
    __tablename__ = 'pedido_items'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    nombre_item = db.Column(db.String(255), nullable=False)
    descripcion_item = db.Column(db.Text)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(10,2), nullable=False)
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla de Reseñas
class Reseña(db.Model):
    __tablename__ = 'reseñas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'))
    calificacion = db.Column(db.Integer, nullable=False)  # 1-5
    titulo = db.Column(db.String(200))
    comentario = db.Column(db.Text)
    ventajas = db.Column(db.Text)
    desventajas = db.Column(db.Text)
    recomendaria = db.Column(db.Boolean)
    foto_resena = db.Column(db.String(500))
    estado = db.Column(db.Enum('pendiente', 'aprobada', 'rechazada'), default='pendiente')
    util_si = db.Column(db.Integer, default=0)
    util_no = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# ====================================================
# NUEVAS TABLAS ADICIONALES
# ====================================================

# Tabla de Categorías de Menú
class CategoriaMenu(db.Model):
    __tablename__ = 'categorias_menu'
    id = db.Column(db.Integer, primary_key=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    orden = db.Column(db.Integer, default=0)
    visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    menu_items = db.relationship('MenuItem', backref='categoria', lazy=True, cascade='all, delete-orphan')

# Tabla de Items de Menú
class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_menu.id'))
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    precio_descuento = db.Column(db.Numeric(10,2))
    categoria = db.Column(db.String(100))
    subcategoria = db.Column(db.String(100))
    imagen_url = db.Column(db.String(500))
    disponible = db.Column(db.Boolean, default=True)
    tiempo_preparacion = db.Column(db.Integer)  # minutos
    calorias = db.Column(db.Integer)
    vegetariano = db.Column(db.Boolean, default=False)
    vegano = db.Column(db.Boolean, default=False)
    sin_gluten = db.Column(db.Boolean, default=False)
    picante = db.Column(db.Boolean, default=False)
    destacado = db.Column(db.Boolean, default=False)
    orden = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    pedido_items = db.relationship('PedidoItem', backref='menu_item', lazy=True)

# Tabla de Horarios de Restaurantes
class HorarioRestaurante(db.Model):
    __tablename__ = 'horarios_restaurantes'
    id = db.Column(db.Integer, primary_key=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    dia_semana = db.Column(db.Enum('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'), nullable=False)
    hora_apertura = db.Column(db.Time, nullable=False)
    hora_cierre = db.Column(db.Time, nullable=False)
    abierto = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Índice único para evitar duplicados
    __table_args__ = (db.UniqueConstraint('restaurante_id', 'dia_semana', name='unique_horario_restaurante'),)

# Tabla de Direcciones de Usuarios
class DireccionUsuario(db.Model):
    __tablename__ = 'direcciones_usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    alias = db.Column(db.String(100))
    direccion = db.Column(db.Text, nullable=False)
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(10))
    latitud = db.Column(db.Numeric(10, 8))
    longitud = db.Column(db.Numeric(11, 8))
    instrucciones = db.Column(db.Text)
    predeterminada = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla de Métodos de Pago
class MetodoPago(db.Model):
    __tablename__ = 'metodos_pago'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo = db.Column(db.Enum('tarjeta_credito', 'tarjeta_debito', 'paypal', 'efectivo', 'transferencia'), nullable=False)
    proveedor = db.Column(db.String(50))
    numero_tarjeta = db.Column(db.String(20))
    nombre_titular = db.Column(db.String(200))
    fecha_expiracion = db.Column(db.Date)
    cvv = db.Column(db.String(4))
    email_pago = db.Column(db.String(255))
    predeterminado = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla de Promociones y Descuentos
class Promocion(db.Model):
    __tablename__ = 'promociones'
    id = db.Column(db.Integer, primary_key=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'))
    codigo_promo = db.Column(db.String(50), unique=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    tipo_descuento = db.Column(db.Enum('porcentaje', 'fijo', 'envio_gratis'), nullable=False)
    valor_descuento = db.Column(db.Numeric(10,2), nullable=False)
    tipo_uso = db.Column(db.Enum('unico', 'multiple'), default='multiple')
    limite_usos = db.Column(db.Integer, default=0)
    usos_actuales = db.Column(db.Integer, default=0)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)
    minimo_compra = db.Column(db.Numeric(10,2), default=0.00)
    maximo_descuento = db.Column(db.Numeric(10,2))
    aplicable_envio = db.Column(db.Boolean, default=False)
    aplicable_recoger = db.Column(db.Boolean, default=False)
    aplicable_local = db.Column(db.Boolean, default=False)
    estado = db.Column(db.Enum('activo', 'inactivo', 'agotado', 'expirado'), default='activo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    usos = db.relationship('UsoPromocion', backref='promocion', lazy=True, cascade='all, delete-orphan')

class UsoPromocion(db.Model):
    __tablename__ = 'uso_promociones'
    id = db.Column(db.Integer, primary_key=True)
    promocion_id = db.Column(db.Integer, db.ForeignKey('promociones.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'))
    codigo_usado = db.Column(db.String(50))
    descuento_aplicado = db.Column(db.Numeric(10,2))
    fecha_uso = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla de Notificaciones
class Notificacion(db.Model):
    __tablename__ = 'notificaciones'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'))
    tipo = db.Column(db.Enum('reserva_confirmada', 'reserva_cancelada', 'pedido_nuevo', 'pedido_listo', 'pedido_enviado', 'pedido_entregado', 'promocion', 'reseña', 'general'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    leida = db.Column(db.Boolean, default=False)
    importante = db.Column(db.Boolean, default=False)
    enlace = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla de Tickets de Soporte
class TicketSoporte(db.Model):
    __tablename__ = 'tickets_soporte'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    admin_asignado_id = db.Column(db.Integer, db.ForeignKey('administradores.id'))
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'))
    codigo_ticket = db.Column(db.String(20), unique=True)
    asunto = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.Enum('baja', 'media', 'alta', 'urgente'), default='media')
    categoria = db.Column(db.Enum('tecnico', 'facturacion', 'cuenta', 'pedido', 'reserva', 'restaurante', 'general'), nullable=False)
    estado = db.Column(db.Enum('abierto', 'en_progreso', 'esperando_respuesta', 'cerrado', 'cancelado'), default='abierto')
    origen = db.Column(db.Enum('usuario', 'restaurante', 'admin', 'sistema'), default='usuario')
    adjuntos = db.Column(db.JSON)  # URLs de archivos adjuntos
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime)

# Tabla de Administradores
class Administrador(db.Model):
    __tablename__ = 'administradores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    foto_perfil = db.Column(db.String(500))
    departamento = db.Column(db.String(100))
    fecha_contratacion = db.Column(db.Date)
    salario = db.Column(db.Numeric(10,2))
    fecha_ultimo_login = db.Column(db.DateTime)
    ultimo_ip_login = db.Column(db.String(45))
    estado = db.Column(db.Enum('activo', 'inactivo', 'suspendido'), default='activo')
    verificado = db.Column(db.Boolean, default=False)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    tickets_asignados = db.relationship('TicketSoporte', backref='admin_asignado', lazy=True)
    notificaciones = db.relationship('Notificacion', backref='administrador', lazy=True)

# Tabla de Configuración del Sistema
class ConfiguracionSistema(db.Model):
    __tablename__ = 'configuracion_sistema'
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text)
    tipo = db.Column(db.Enum('texto', 'numero', 'booleano', 'json'), default='texto')
    descripcion = db.Column(db.String(500))
    grupo = db.Column(db.String(50))
    editable = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Tabla de Backups del Sistema
class BackupSistema(db.Model):
    __tablename__ = 'system_backups'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('administradores.id'))
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta_archivo = db.Column(db.String(500), nullable=False)
    tamaño_bytes = db.Column(db.BigInteger, nullable=False)
    tipo_backup = db.Column(db.Enum('completo', 'incremental', 'base_datos', 'archivos'), nullable=False)
    estado = db.Column(db.Enum('completado', 'fallido', 'en_progreso'), default='en_progreso')
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_finalizacion = db.Column(db.DateTime)
    duracion_segundos = db.Column(db.Integer)
    mensaje_error = db.Column(db.Text)

# Tabla de Logs del Sistema
class LogSistema(db.Model):
    __tablename__ = 'system_logs'
    id = db.Column(db.Integer, primary_key=True)
    nivel = db.Column(db.Enum('debug', 'info', 'warning', 'error', 'critical'), nullable=False)
    componente = db.Column(db.String(100), nullable=False)  # api, database, auth, etc.
    mensaje = db.Column(db.Text, nullable=False)
    datos_contexto = db.Column(db.JSON)  # Datos adicionales del contexto
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('administradores.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla de Métricas del Sistema
class MetricaSistema(db.Model):
    __tablename__ = 'system_metrics'
    id = db.Column(db.Integer, primary_key=True)
    metrica_nombre = db.Column(db.String(100), nullable=False)
    valor_numerico = db.Column(db.Numeric(15,4))
    valor_texto = db.Column(db.Text)
    unidad_medida = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    periodo_agregacion = db.Column(db.Enum('hora', 'dia', 'semana', 'mes'), default='dia')

# Tabla de Banners Promocionales
class BannerPromocional(db.Model):
    __tablename__ = 'banners_promocionales'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    imagen_url = db.Column(db.String(500), nullable=False)
    link_destino = db.Column(db.String(500))
    tipo_banner = db.Column(db.Enum('principal', 'secundario', 'emergente', 'movil'), default='principal')
    posicion = db.Column(db.Enum('top', 'middle', 'bottom', 'sidebar'), default='top')
    activo = db.Column(db.Boolean, default=True)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    orden_visualizacion = db.Column(db.Integer, default=0)
    target_audience = db.Column(db.JSON)  # Público objetivo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Tabla de Contenido Estático
class ContenidoEstatico(db.Model):
    __tablename__ = 'contenido_estatico'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    tipo_contenido = db.Column(db.Enum('pagina', 'faq', 'terminos', 'privacidad', 'blog', 'newsletter'), nullable=False)
    categoria = db.Column(db.String(100))
    meta_titulo = db.Column(db.String(255))
    meta_descripcion = db.Column(db.Text)
    keywords = db.Column(db.Text)
    autor_id = db.Column(db.Integer, db.ForeignKey('administradores.id'))
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = db.Column(db.Enum('borrador', 'publicado', 'archivado'), default='borrador')
    vistas = db.Column(db.Integer, default=0)