
# Define operaciones de entradas
from flask_app.config.mysqlconnection import connectToMySQL

class Entrada:
    def __init__(self, data):
        self.id_entrada = data['id_entrada']
        self.fecha_entrada = data['fecha_entrada']
        self.nota = data['nota']
        self.id_usuario = data['id_usuario']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO entradas (fecha_entrada, nota, id_usuario)
            VALUES (%(fecha_entrada)s, %(nota)s, %(id_usuario)s);
        """
        return connectToMySQL('querido_diario').query_db(query, data)
    
    @classmethod
    def get_by_usuario(cls, data):
        query = """
            SELECT * FROM entradas
            WHERE id_usuario = %(id_usuario)s
            ORDER BY fecha_entrada DESC;
        """
        resultados = connectToMySQL('querido_diario').query_db(query, data)

        entradas = []
        for resultado in resultados:
            entradas.append(cls(resultado))

        return entradas
    
    # Buscar una entrada por su ID y el ID de su dueño
    @classmethod
    def get_by_id_usuario(cls, data):
        query = """
            SELECT * FROM entradas
            WHERE id_entrada = %(id_entrada)s
            AND id_usuario = %(id_usuario)s;
        """
        resultado = connectToMySQL('querido_diario').query_db(query, data)

        if resultado:
            return cls(resultado[0])

        return None

    # Actualizar una entrada únicamente si pertenece al usuario
    @classmethod
    def update(cls, data):
        query = """
            UPDATE entradas
            SET fecha_entrada = %(fecha_entrada)s,
                nota = %(nota)s
            WHERE id_entrada = %(id_entrada)s
            AND id_usuario = %(id_usuario)s;
        """
        return connectToMySQL('querido_diario').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = """
            DELETE FROM entradas
            WHERE id_entrada = %(id_entrada)s
            AND id_usuario = %(id_usuario)s;
        """
        return connectToMySQL('querido_diario').query_db(query, data)

    # Validar los mismos campos al crear y editar
    @staticmethod
    def validar_entrada(data):
        fecha = data.get('fecha_entrada', '')
        nota = data.get('nota', '').strip()

        if not fecha or not nota:
            return False

        return True

    @classmethod
    def buscar_por_usuario(cls, data):
        query = """
            SELECT * FROM entradas
            WHERE id_usuario = %(id_usuario)s
            AND nota LIKE %(termino)s
            ORDER BY fecha_entrada DESC;
        """

        datos = {
            'id_usuario': data['id_usuario'],
            'termino': '%' + data['termino'].strip() + '%'
        }

        resultado = connectToMySQL('querido_diario').query_db(query, datos)

        entradas = []

        if resultado:
            for fila in resultado:
                entradas.append(cls(fila))

        return entradas
