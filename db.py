import psycopg2


class Database:
    def __init__(
        self, database="db_name", host="db_host", user="db_user", password="db_pass", port="db_port"
    ):
        self.conn = psycopg2.connect(
            database=database, host=host, user=user, password=password, port=port
        )

    def register(self, user):
        cursor = self.conn.cursor()
        query = "SELECT register(%s, %s, %s);"
        parametros = (user['name'],user['password'], user['rol'])
        cursor.execute(query, parametros)
        response = cursor.fetchall()
        cursor.close()
        return response
    
    def login(self, user):
        cursor = self.conn.cursor()
        query = "SELECT login(%s, %s);"
        parametros = (user['name'],user['password'])
        cursor.execute(query, parametros)
        result = cursor.fetchone()#Lo que retorno la funcion de postgres
        cursor.close()
        return {"code": result}
    
    def get_users(self):
        cursor = self.conn.cursor()
        query = "SELECT id, nombre, pass, idrol FROM usuario;"
        cursor.execute(query)
        result = cursor.fetchall()#Lo que retorno la funcion de postgres
        cursor.close()
        return result
    
    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM usuario WHERE id = {user_id};")
        data = cursor.fetchall()
        cursor.close()
        return data


    def update_user(self, request_user):
        cursor = self.conn.cursor()
        query = "SELECT update_user(%(id)s,%(name)s,%(password)s,%(rol)s);"
        cursor.execute(query, request_user)
        self.conn.commit()
        cursor.close()
        return request_user

    def delete_user(self, request_user_id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM usuario WHERE id = {request_user_id};")
        user_deleted = cursor.fetchall()#Lo que retorno la funcion de postgres
        cursor.execute(f"DELETE FROM usuario WHERE id = {request_user_id};")
        self.conn.commit()
        cursor.close()
        return user_deleted
