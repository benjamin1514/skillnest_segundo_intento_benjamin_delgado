from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
nombre_regex = re.compile(r'^[a-zA-Z]+$')
apellido_regex = re.compile(r'^[a-zA-Z]+$')

class Usuario:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password_hash = data['password_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # valida los datos del usuario, si no cumple con los requisitos manda un mensaje de error
    @staticmethod
    def validar_usuario(usuario):
        is_valid = True
        if not nombre_regex.match(usuario['nombre']):
            flash("El nombre solo puede contener letras.", "error_nombre")
            is_valid = False
        if not apellido_regex.match(usuario['apellido']):
            flash("El apellido solo puede contener letras.", "error_apellido")
            is_valid = False
        if not email_regex.match(usuario['email']):
            flash("Correo electrónico inválido.", "error_email")
            is_valid = False
        if len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error_password")
            is_valid = False
        if usuario['password'] != usuario['confirm_password']:
            flash("Las contraseñas no coinciden.", "error_confirm_password")
            is_valid = False
        return is_valid

    # permite guardar un usuario en la base de datos
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password_hash)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password_hash)s);
        """
        return connectToMySQL('querido_diario').query_db(query, data)

    # permite obtener un usuario por su correo electrónico
    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL('querido_diario').query_db(query, {'email': email})
        if result:
            return cls(result[0])
        return None

    # permite obtener un usuario por su id
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM usuarios WHERE id_usuario = %(id_usuario)s;"
        result = connectToMySQL('querido_diario').query_db(query, {'id_usuario': id})
        if result:
            return cls(result[0])
        return None