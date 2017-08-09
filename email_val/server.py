from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app, 'mydb')

def validateEmail(email):
	if len(email) > 7:
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
			return 1
	return 0

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

    if match == 0:
        return render_template('index.html',Valid=False)
    elif match == 1:
        # this code for valid emails
        #INSERT INTO query
        query = "INSERT INTO emails (name,created_at, updated_at) VALUES (:name,NOW(),NOW())"
        data = {'name': addressToVerify}
        emails = mysql.query_db(query,data)
        query = "SELECT * from emails"
        emails = mysql.query_db(query)
        return render_template('success.html', emails=emails, tested=addressToVerify)

app.run(debug=True)
