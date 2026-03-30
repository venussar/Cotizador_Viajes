from .entities.user import User
from werkzeug.security import generate_password_hash

# Clase para manejar operaciones relacionadas con el usuario en la base de datos
class ModelUser:
    @staticmethod
    def login(db, email, password):
        """
        Autentica un usuario usando email y password.
        Args:
            db: conexión a la base de datos
            email: email del usuario
            password: contraseña ingresada
        Returns:
            user_db: objeto usuario si la autenticación es exitosa, None si falla
        """
        try:
            # Crear cursor para ejecutar consultas SQL
            cursor = db.connection.cursor()
            # Consulta para obtener datos del usuario por email
            sql = """
SELECT id, namee, email, ` password_hash`
FROM users
WHERE email = %s
"""
            # Ejecutar consulta con parámetro seguro
            cursor.execute(sql, (email,))
            row = cursor.fetchone()
            # Si se encuentra el usuario
            if row is not None:
                # Crear objeto usuario con los datos obtenidos
                user_db = User(row[0], row[1], row[2], row[3])
                # Verificar la contraseña ingresada contra el hash almacenado
                if User.check_password(user_db.password_hash, password):
                    return user_db  # Autenticación exitosa
            # Si no se encuentra el usuario o la contraseña es incorrecta
            return None
        except Exception as ex:            # Re-lanzar la excepción para manejo externo
            raise ex

    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, namee, email, ` password_hash` FROM users WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], row[2], row[3])
            else:
                return None
        except Exception as ex:
            raise ex

    @staticmethod
    def create_user(db, name, email, password, role='cotizador'):
        try:
            cursor = db.connection.cursor()
            hashed_password = generate_password_hash(password)
            sql = "INSERT INTO users (namee, email, password_hash, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, email, hashed_password, role))
            db.connection.commit()
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all(db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, namee, email, role FROM users"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except Exception as ex:
            raise ex

    @staticmethod
    def update_user(db, user_id, name, email, role, password=None):
        try:
            cursor = db.connection.cursor()
            if password:
                hashed_password = generate_password_hash(password)
                sql = "UPDATE users SET namee = %s, email = %s, role = %s, password_hash = %s WHERE id = %s"
                cursor.execute(sql, (name, email, role, hashed_password, user_id))
            else:
                sql = "UPDATE users SET namee = %s, email = %s, role = %s WHERE id = %s"
                cursor.execute(sql, (name, email, role, user_id))
            db.connection.commit()
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_user(db, user_id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            db.connection.commit()
        except Exception as ex:
            raise ex