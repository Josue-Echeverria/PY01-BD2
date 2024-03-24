import json

from db import Database


class AppService:

    def __init__(self, database: Database):
        self.database = database

    def get_tasks(self):
        data = self.database.get_tasks()
        return data

    def get_task_by_id(self, task_id: int):
        """Get a task by its id.

        Args:
            task_id (int): The id of the task.
        """
        data = self.database.get_task_by_id(task_id)
        return data

    def create_task(self, task):
        self.database.create_task(task)
        return task

    def update_task(self, request_task):
        self.database.update_task(request_task)
        return request_task

    def delete_task(self, request_task_id):
        self.database.delete_task(request_task_id)
        return request_task_id
