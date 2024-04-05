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
        query = "SELECT * from login(%s, %s);"
        parametros = (user['name'],user['password'])
        cursor.execute(query, parametros)
        result = cursor.fetchone()#Lo que retorno la funcion de postgres
        cursor.close()
        return {"code": result}
    
    def get_users(self):
        cursor = self.conn.cursor()
        query = "SELECT id, nombre, pass, idrol FROM public.usuario;"
        # parametros = (user['name'],user['password'])
        cursor.execute(query)
        result = cursor.fetchall()#Lo que retorno la funcion de postgres
        cursor.close()
        return result
    

    def get_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks;")
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_task_by_id(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM tasks WHERE id = {task_id};")
        data = cursor.fetchall()
        cursor.close()
        return data

    def create_task(self, task):
        cursor = self.conn.cursor()
        query = "SELECT create_task(%s, %s, %s, %s, %s);"
        parametros = (task['name'],task['description'], task['due_date'], task['Idestado'], task['Idusuario'])
        cursor.execute(query, parametros)
        result = cursor.fetchone()#Lo que retorno la funcion de postgres
        retursStatement = {}
        if(result == 1):
            retursStatement = task
        elif(result == 5001):
            retursStatement = {"usuario": "null"}
        cursor.close()
        return retursStatement

    def update_task(self, request_task):
        cursor = self.conn.cursor()
        cursor.execute(
            f"UPDATE tasks SET name = '{request_task['name']}', description = '{request_task['description']}' WHERE id = {request_task['id']};"
        )
        self.conn.commit()
        cursor.close()
        return request_task

    def delete_task(self, request_task_id):
        cursor = self.conn.cursor()
        cursor.execute(f"DELETE FROM tasks WHERE id = {request_task_id};")
        self.conn.commit()
        cursor.close()
        return request_task_id
