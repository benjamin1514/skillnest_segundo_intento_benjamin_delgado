from flask_app.config.mysqlconnection import connectToMySQL

class Entrada:
    def __init__(self, data):
        self.id_entrada = data['id_entrada']
        self.fecha_entrada = data['fecha_entrada']
        self.notas = data['notas']
        self.id_usuario = data['id_usuario']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # permite guardar una entrada en la base de datos
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO entradas (fecha_entrada, notas, id_usuario)
            VALUES (%(fecha_entrada)s, %(notas)s, %(id_usuario)s);
        """
        return connectToMySQL('CinePedia').query_db(query, data)
    