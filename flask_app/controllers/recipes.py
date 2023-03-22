from flask_app import app
from flask import render_template,session,redirect,request
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask import flash

@app.route("/recipe/create")
def recipe_create():
    return render_template("recipe_creation.html")

@app.route("/recipes/new", methods=["post"])
def created_recipe():
    if not Recipe.validate(request.form):# if its true that its false
        return redirect("/recipe/create")
    Recipe.create_recipe(request.form)
    return redirect("/logged")

@app.route("/recipes/<int:id>")
def show_one(id):
    if 'user_id' not in session:
        return redirect("/")
    this_recipe=Recipe.get_one_recipe(id)
    this_user=User.get_one(session['user_id'])
    return render_template("recipe_show.html",this_recipe=this_recipe,this_user=this_user)

@app.route("/recipes/edit/<int:id>")
def edit_page(id):
    edit_recipe=Recipe.get_one_recipe(id)
    return render_template("recipe_edit.html",edit_recipe=edit_recipe)

@app.route("/recipes/edit",methods =['post'])
def edit_recipe():
    if not Recipe.validate(request.form):# if its true that its false
        return redirect(f"/recipes/edit/{request.form['id']}")
    Recipe.edit(request.form)
    return redirect("/logged")

@app.route("/recipes/delete/<int:id>")
def del_recipe(id):
    Recipe.delete({'id':id})
    return redirect("/logged")
