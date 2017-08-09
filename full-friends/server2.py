from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')
@app.route('/')
def index():
    query = "SELECT * from friends"
    friends = mysql.query_db(query)
    return render_template('index2.html', all_friends=friends)

@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friends (first_name, last_name, age, created_at, updated_at) VALUES (:first_name, :last_name, :age, NOW(), NOW())"
    data = {
        'first_name': request.form['first_name'],
        'last_name':  request.form['last_name'],
        'age': request.form['age']
    }
    print data['age']
    print request.form['age']
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<friend_id>')
def show(friend_id):
    query = "SELECT * FROM friends WHERE id = :specific_id"
    data = {'specific_id': friend_id}
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('index2.html', one_friend=friends[0])


@app.route('/edit_friend/<friend_id>')
def edit(friend_id):
    query = "SELECT * from friends WHERE id = :id"
    data = {
        'id': friend_id
    }
    friends = mysql.query_db(query, data)
    return render_template('index2.html', one_friend=friends[0],edit=True)


@app.route('/update_friend/<friend_id>', methods=['POST'])
def update(friend_id):
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, age = :age WHERE id = :id"
    data = {
        'first_name': request.form['first_name'],
        'last_name':  request.form['last_name'],
        'age': request.form['age'],
        'id': friend_id
    }
    mysql.query_db(query, data)
    query = "SELECT * FROM friends WHERE id = :specific_id"
    data = {'specific_id': friend_id}
    friends = mysql.query_db(query, data)
    return render_template('index2.html', one_friend=friends[0])

@app.route('/remove_friend/<friend_id>', methods=['POST'])
def delete(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)
