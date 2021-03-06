from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app, 'friendsdb')
EMAIL_REGEX = re.compile(r'"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"')
app.secret_key = "ITsASecretkEy"

@app.route('/')
def index():
    query = "SELECT * from friends"
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends=friends)


@app.route('/users/new')
def new():
    return render_template('edit.html')

@app.route('/users/create', methods=['POST'])
def create():
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    data = {
        'first_name': request.form['first_name'],
        'last_name':  request.form['last_name'],
        'email': request.form['email']
    }
    print data['email']
    print request.form['email']
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/users/<friend_id>')
def show(friend_id):
    query = "SELECT * FROM friends WHERE id = :specific_id"
    data = {'specific_id': friend_id}
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('index.html', one_friend=friends[0])


@app.route('/users/<friend_id>/edit')
def edit(friend_id):
    query = "SELECT * from friends WHERE id = :id"
    data = {
        'id': friend_id
    }
    friends = mysql.query_db(query, data)
    return render_template('index.html', one_friend=friends[0],edit=True)


@app.route("/users/<friend_id>", methods=['POST'])
def update(friend_id):
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"
    data = {
        'first_name': request.form['first_name'],
        'last_name':  request.form['last_name'],
        'email': request.form['email'],
        'id': friend_id
    }
    mysql.query_db(query, data)
    query = "SELECT * FROM friends WHERE id = :specific_id"
    data = {'specific_id': friend_id}
    friends = mysql.query_db(query, data)
    return render_template('index.html', one_friend=friends[0])


@app.route('/users/<friend_id>/destroy')
def destroy(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    if mysql.query_db(query, data):
        print "it worked"
    else:
        print "IT DIDN'T Work"
    return redirect('/')

app.run(debug=True)
