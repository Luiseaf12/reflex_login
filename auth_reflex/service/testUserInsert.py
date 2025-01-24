from ..models import User
import bcrypt
import reflex as rx
from sqlmodel import Session

def insert_test_users():
    """
    Inserta 5 usuarios de prueba en la base de datos.
    Retorna la lista de usuarios creados.
    """
    
    # Crear contraseña encriptada
    password = "password123"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    
    test_users = [
        User(username="usuario1@test.com", password=hashed.decode()),
        User(username="usuario2@test.com", password=hashed.decode()),
        User(username="usuario3@test.com", password=hashed.decode()),
        User(username="usuario4@test.com", password=hashed.decode()),
        User(username="usuario5@test.com", password=hashed.decode())
    ]
    
    with rx.session() as session:
        for user in test_users:
            session.add(user)
        session.commit()
        
        print("Usuarios de prueba creados exitosamente:")
        for user in test_users:
            # Refrescar el objeto dentro de la sesión
            session.refresh(user)
            print(f"Usuario: {user.username} - Contraseña: password123")
    
    return "Usuarios creados exitosamente"

if __name__ == "__main__":
    insert_test_users()