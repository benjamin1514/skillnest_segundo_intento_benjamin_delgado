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
        return connectToMySQL('querido_diario').query_db(query, data)
    
    @classmethod
    def get_by_usuario(cls, data):
        query = "SELECT * FROM entradas WHERE id_usuario = %(id_usuario)s;"
        result = connectToMySQL('querido_diario').query_db(query, data)
        entradas = []
        for entrada in result:
            entradas.append(cls(entrada))
        return entradas
    
    