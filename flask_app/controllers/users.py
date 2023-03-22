from flask_app import app
from flask import render_template,session,redirect,request
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users/register", methods=["POST"])
def register():
    if not User.validate(request.form):# if its true that its false
        return redirect("/")
    new_password=bcrypt.generate_password_hash(request.form['password'])
    user_data ={
        **request.form,
        'password' : new_password
    }
    user_id =User.create(user_data)
    session['user_id'] = user_id
    return redirect("/logged")


@app.route("/logged")
def logged():
    if 'user_id' not in session:
        return redirect("/")
    this_user=User.get_one(session['user_id'])
    all_recipes = Recipe.get_all()
    return render_template("logged.html",this_user=this_user,all_recipes=all_recipes)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/user/login", methods=['post'])
def user_log():
    user_email=User.get_email(request.form['email'])
    if not user_email:
        flash("invalid credentials","login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_email.password,request.form['password']):
        flash("invalid credentials","login")
        return redirect("/")
    session['user_id'] = user_email.id
    return redirect("/logged")