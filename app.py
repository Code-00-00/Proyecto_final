# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/final_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Usuario
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
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Crear tablas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    user_logged_in = 'user_id' in session
    user_name = session.get('user_name', '')
    return render_template('index.html', 
                         user_logged_in=user_logged_in, 
                         user_name=user_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = f"{user.nombre} {user.apellido}"
            flash('¡Bienvenido de vuelta!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
    
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        password = request.form.get('password')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        ciudad = request.form.get('ciudad')
        codigo_postal = request.form.get('codigo_postal')
        genero = request.form.get('genero')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        
        # Verificar si el email ya existe
        email_exists = Usuario.query.filter_by(email=email).first()
        if email_exists:
            flash('Este correo electrónico ya está registrado.', 'error')
            return render_template('index.html')
        
        # Crear nuevo usuario
        new_user = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            direccion=direccion,
            ciudad=ciudad,
            codigo_postal=codigo_postal,
            genero=genero,
            fecha_nacimiento=fecha_nacimiento if fecha_nacimiento else None
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f'¡Bienvenido {nombre}! Tu cuenta ha sido creada exitosamente.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la cuenta. Inténtalo de nuevo.', 'error')
            return render_template('index.html')
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)