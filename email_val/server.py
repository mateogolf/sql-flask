from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app, 'mydb')

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/return')
def home():
    return redirect('/')

@app.route('/tested', methods=['POST'])
def test():
    addressToVerify = request.form['email']
    match = validateEmail(addressToVerify)
    #If comparing to database
    # query = "SELECT id from emails WHERE name= :name"
    # data = {'name': addressToVerify}
    # input_IDs = mysql.query_db(query, data)
    # print input_IDs
    # if mysql.query_db(query, data):
        # print "Email already exists"


    if not match: #Input is invalid
        return render_template('index.html', tested=addressToVerify, Valid=False)
    else:
        # this code for valid emails
        #INSERT INTO query
        query = "INSERT INTO emails (name,created_at, updated_at) VALUES (:name,NOW(),NOW())"
        data = {'name': addressToVerify}
        emails = mysql.query_db(query,data)
        query = "SELECT * from emails"
        emails = mysql.query_db(query)
        return render_template('success.html', emails=emails, tested=addressToVerify)

app.run(debug=True)
