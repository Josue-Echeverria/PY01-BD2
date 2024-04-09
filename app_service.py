import json

from db import Database


class AppService:

    def __init__(self, database: Database):
        self.database = database

    def register(self, user):
        response = self.database.register(user)
        return response

    def login(self, user):
        response = self.database.login(user)
        return response

    def get_users(self):
        response = self.database.get_users()
        return response

    def get_user_by_id(self, user_id: int):
        data = self.database.get_user_by_id(user_id)
        return data

    def create_user(self, user):
        self.database.create_user(user)
        return user

    def update_user(self, request_user):
        self.database.update_user(request_user)
        return request_user

    def delete_user(self, request_user_id):
        deleted_user = self.database.delete_user(request_user_id)
        return deleted_user

# ENCUESTADOS

    def get_respondents(self):
        response = self.database.get_respondents()
        return response

    def get_respondents_by_id(self, respondents_id: int):
        data = self.database.get_respondents_by_id(respondents_id)
        return data
    
    def register_respondents(self, respondents):
        response = self.database.register_respondents(respondents)
        return response

    def update_respondents(self, request_respondents):
        self.database.update_respondents(request_respondents)
        return request_respondents

    def delete_respondents(self, request_respondents_id):
        deleted_respondents = self.database.delete_respondents(request_respondents_id)
        return deleted_respondents

