from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model


class Recipe:
    def __init__(self,data) -> None:
        self.id=data['id']
        self.name=data['name']
        self.description=data['description']
        self.instructions=data['instructions']
        self.made=data['made']
        self.undertime=data['undertime']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']


    @classmethod
    def create_recipe(cls,data):
        query="""
        INSERT INTO recipes
            (name,description,instructions,made,undertime,user_id)
        VALUES
        (%(name)s,%(description)s,%(instructions)s,%(made)s,%(undertime)s,%(user_id)s);
        """
        return connectToMySQL('recipe').query_db(query,data)
    
    @classmethod
    def get_one_recipe(cls,id):
        data = {
            'id' : id
        }
        query="""
        SELECT * FROM recipes
        JOIN users
        ON users.id = recipes.user_id
        WHERE  recipes.id = %(id)s;
        """
        results =connectToMySQL('recipe').query_db(query,data)
        if results:
            this_recipe = cls(results[0])
            row=results[0]
            user_data={
                **row,
                'id' : row['users.id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            this_user = user_model.User(user_data)
            this_recipe.creations = this_user
            return this_recipe
        return False
    
    @classmethod
    def get_all(cls):
        query="""
        SELECT * FROM recipes
        LEFT JOIN users
        ON users.id = recipes.user_id;
        """
        results=connectToMySQL('recipe').query_db(query)
        all_recipes=[]
        for row in results:
            this_recipe = cls(row)
            user_data={
                **row,
                'id':row['users.id'],
                'created_at ': row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            this_recipe.creations = user_model.User(user_data)
            all_recipes.append(this_recipe)
        return all_recipes
    
    @classmethod
    def edit(cls,data):
        query="""
        UPDATE recipes
        SET 
        name = %(name)s,
        description=%(description)s,
        instructions=%(instructions)s,
        made=%(made)s,
        undertime=%(undertime)s
        WHERE id =%(id)s;
        """
        return connectToMySQL('recipe').query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query="""
            DELETE FROM recipes
            WHERE id=%(id)s 
        """
        return connectToMySQL('recipe').query_db(query,data)
    
    @staticmethod
    def validate(data):
        is_valid=True
        if len(data['name'])<3:
            is_valid=False
            flash("name is required")
        if len(data['description'])<3:
            is_valid=False
            flash("descriptions is required")
        if len(data['instructions'])<3:
            is_valid=False
            flash("instructions is required")
        if len(data['made'])<1:
            is_valid=False
            flash("date is required")
        if 'undertime' not in data:
            is_valid=False
            flash("pick a choice")
        return is_valid