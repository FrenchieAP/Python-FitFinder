import re
from flask_app import app
from flask import render_template,redirect,request,session,flash,jsonify
from flask_app.models.users_model import User
from flask_app.models.gyms_model import Gym
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import requests
import os
from flask import jsonify

@app.route('/api_key')
def api_key():
    return jsonify({"api_key": GOOGLE_API_KEY})

@app.route('/')
def home():
    if 'user_id' in session:
        user_obj = {"id": session["user_id"]}
        user = User.get_by_id(user_obj)
        return render_template("index.html", user = user)
    else:
        return render_template("reg.html")

@app.route('/gym/<string:place_id>')
def show_gym(place_id):
    gym = Gym.get_by_place_id(place_id)
    user = User.get_by_id({"id": session["user_id"]})
    user_id = session['user_id']
    is_favorite = User.is_favorite(user_id, place_id)
    reviews = User.get_reviews_by_gym(place_id)
    return render_template('one_gym.html', gym=gym, user=user, is_favorite = is_favorite, reviews=reviews)

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
        'name' : request.form['name'],
        'place_id' : request.form['place_id']
    }
    User.add_favorite(data)
    return redirect("/favorites")

@app.route("/favorites")
def all_favorites():
    query = "SELECT * FROM favorites WHERE users_id = %(users_id)s;"
    data = {'users_id': session['user_id']}
    results = connectToMySQL(DATABASE).query_db(query,data)
    user = User.get_by_id({"id": session["user_id"]})
    return render_template("favorites.html", fav_list=results, user=user)

@app.route('/favorite/delete/<string:place_id>', methods=['POST'])
def delete_favorite(place_id):
    query = "DELETE FROM favorites WHERE place_id = %(place_id)s AND users_id = %(users_id)s;"
    data = {
        'place_id': place_id,
        'users_id': session['user_id']
    }
    connectToMySQL(DATABASE).query_db(query, data)
    return redirect("/favorites")

@app.route('/review', methods=['POST'])
def add_review():
    data = {
        'user_id' : session['user_id'],
        'place_id' : request.form['place_id'],
        'name' : request.form['name'],
        'rating' : request.form['rating'],
        'comment' : request.form['comment']
    }
    User.add_review(data)
    print(request.form)
    return redirect("/reviews")

@app.route("/reviews")
def all_reviews():
    query = "SELECT * FROM reviews WHERE user_id = %(user_id)s;"
    data = {'user_id': session['user_id']}
    results = connectToMySQL(DATABASE).query_db(query,data)
    user = User.get_by_id({"id": session["user_id"]})
    return render_template("reviews.html", reviews=results, user=user)

@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    # Optional: Check if the current user is authorized to delete this review
    # ...

    # Call a method to delete the review
    User.delete_review(review_id)

    # Redirect to the reviews page or another appropriate page after deletion
    return redirect("/reviews")
    

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
    del session['user_id']
    return redirect('/')

@app.route('/test_db')
def test_db():
    try:
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            return jsonify(results)
        else:
            return "No data found or there's an issue with the query."
    except Exception as e:
        return f"Error: {str(e)}"