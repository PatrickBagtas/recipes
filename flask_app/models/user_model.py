from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX =re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls,data):
        query = """
        INSERT INTO users
            (first_name, last_name, email, password)
        VALUES 
            (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL('recipe').query_db(query,data)
    
    @classmethod
    def get_one(cls,id):
        data = {
            'id' : id
        }
        query = """
            SELECT * FROM users
            WHERE id = %(id)s;
        """
        results=connectToMySQL('recipe').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_email(cls,email):
        data = {
            'email' :email
        }
        query = """
            SELECT * FROM users
            WHERE email = %(email)s;
        """
        results=connectToMySQL('recipe').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name'])<2:
            is_valid =False
            flash("first name must have at least 2 characters.","reg")

        if len(data['last_name'])<2:
            is_valid =False
            flash("last_name must ahve at least 2 characters.","reg")

        if len(data['email'])<3:
            is_valid =False
            flash("email must have at least 3 characters.","reg")

        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!","reg")
            is_valid = False
        else:
            valid_user = User.get_email(data['email'])
            if valid_user:
                is_valid = False
                flash("Email in use","reg")

        if len(data['password'])<8:
            is_valid =False
            flash("password must  have at least 8 characters.","reg")
        if not any(char.isupper()for char in data['password']):
            is_valid=False
            flash("Password must have at least one uppcare letter","reg")
        if not any(char.isdigit() for char in data['password']):
            is_valid=False
            flash("Password must have a numeral in password","reg")
        elif not data['password'] == data['confirm_password']:
            is_valid =False
            flash("passwords must match","reg")
        return is_valid
