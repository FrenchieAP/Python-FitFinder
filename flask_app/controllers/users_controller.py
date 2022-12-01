import re
from flask_app import app
from flask import render_template,redirect,request,session,flash,jsonify
from flask_app.models.users_model import User
from flask_app.models.gyms_model import Gym
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import requests
import os

@app.route('/')
def home():
    user = User.get_by_id({"id": session["user_id"]})
    return render_template("index.html", user = user)

@app.route('/one_gym')
def one_gym():
    return render_template("one_gym.html")

@app.route('/reg')
def register():
    return render_template("reg.html")

# @app.route('/search')
# def search():
#     return render_template('search.html')

@app.route('/searching', methods=["POST"])
def search():
    find = request.form["find"]
    near = request.form["near"]
    return redirect (f'/searching/{find}/{near}')

@app.route('/searching/<string:find>/<string:near>')
def searching(find, near):
    gym_list = Gym.get_results(find, near)
    params = {
        "find": find,
        "near" : near
    }
    user = User.get_by_id({"id": session["user_id"]})
    return render_template("search.html", gym_list = gym_list, params = params, user = user)

@app.route('/users/register', methods=['POST'])
def reg_user():
    if not User.validator(request.form):
        return redirect('/reg')
    hash_browns = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hash_browns
    }
    new_id = User.create(data)
    session['user_id'] = new_id
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    # if not User.validator(request.form):
    #     return redirect('/')
    # hash_browns = bcrypt.generate_password_hash(request.form['password'])
    # data = {
    #     **request.form,
    #     'password': hash_browns
    # }
    # new_id = User.create(data)
    # session['user_id'] = new_id
    return render_template("dashboard.html")

@app.route ('/login')  
def login():
    return render_template('login.html')

@app.route('/favorite', methods=['POST'])
def add_favorite():
    data = {
        'users_id' : session['user_id'],
        'place_id' : request.form['place_id']
    }
    User.add_favorite(data)
    return redirect("/favorites")

@app.route("/favorites")
def all_favorites():
    fav_list = User.get_all_favs()
    return render_template("favorites.html", fav_list = fav_list)

@app.route ('/users/login', methods=['POST'])
def log_user():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid credentials", "log")
        return redirect ('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Credentials **", "log")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect('/')

@app.route('/users/logout')
def log_out_user():
    del session[user]
    return redirect('/')
