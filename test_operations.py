# test_operations.py
from app import app
from models import db, Usuario, Restaurante

def test_basic_operations():
    with app.app_context():
        # Crear un usuario de prueba
        usuario = Usuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan@test.com"
        )
        usuario.set_password("123456")
        
        # Guardar en base de datos
        db.session.add(usuario)
        db.session.commit()
        print("✅ Usuario creado exitosamente!")
        
        # Crear un restaurante de prueba
        restaurante = Restaurante(
            nombre="Restaurante Prueba",
            descripcion="Descripción de prueba",
            tipo_cocina="italiana"
        )
        
        # Guardar en base de datos
        db.session.add(restaurante)
        db.session.commit()
        print("✅ Restaurante creado exitosamente!")
        
        # Listar todos los usuarios
        usuarios = Usuario.query.all()
        print(f"👥 Usuarios en la base de datos: {len(usuarios)}")
        for u in usuarios:
            print(f"  - {u.nombre} {u.apellido} ({u.email})")
        
        # Listar todos los restaurantes
        restaurantes = Restaurante.query.all()
        print(f"🏪 Restaurantes en la base de datos: {len(restaurantes)}")
        for r in restaurantes:
            print(f"  - {r.nombre} ({r.tipo_cocina})")

if __name__ == '__main__':
    test_basic_operations()