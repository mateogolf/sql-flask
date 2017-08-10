from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app, 'walldb')
EMAIL_REGEX = re.compile(r'"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$"')
app.secret_key = "ITsASecretkEy"

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False


def validateName(name):
    if len(name) > 2:
        if re.match("^[a-zA-Z]*$", name) != None:
            return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['lemail'],
        'password': request.form['lpassword']
    }
    #Validate that email isn't empty or password is < 8 char
    if len(data['email']) < 1 and len(data['password']) < 8:
        bigLoginError = "Please input a valid email and password to login"
        return render_template('index.html', bigLoginError=bigLoginError)
    # if not EMAIL_REGEX.match(data['email']):
    if not validateEmail(data['email']):
        lemailLogin = "Please input a valid email"
        return render_template('index.html', lemailLogin=lemailLogin)
    if len(data['email']) < 1 and not len(data['password']) < 8:
        lemailLogin = "Input an email"
        return render_template('index.html', lemailLogin=lemailLogin)
    if len(data['password']) < 8 and not len(data['email']) < 1:
        lpasswordLogin = "Input a valid password. 8 char min."
        return render_template('index.html', lpasswordLogin=lpasswordLogin)
    #Validation passes, now find login and password
    query = "SELECT id,email,password,first_name from users WHERE email= :email and password= :password"
    # data = {
    #     'email': request.form['email'],
    #     'password': request.form['password']
    # }
    logins = mysql.query_db(query,data)
    print len(logins)
    if logins:
        #return basic wall page to confirm login
        session['user_id'] = logins[0]['id']
        print '/wall/' + str(session['user_id'])
        return redirect('/wall/'+str(session['user_id']))#render_template('wall.html',user=logins[0])
    else:
        bigLoginError = "Email and Password do not match"
        return render_template('index.html', bigLoginError=bigLoginError)

    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'pw_confirm': request.form['pw_confirm'],
    }
    flag = False
    #Validations:
    # First Name: text only, >2
    if not validateName(data['first_name']):
        flag = True
        flash("First Name must be letters only and longer than 2 chars")
    #Last Name: text only, >2
    if not validateName(data['last_name']):
        flag = True
        flash("Last Name must be letters only and longer than 2 chars")
    # Email REGEX
    if not validateEmail(data['email']):
        flag = True
        flash("Please input a valid email")
    # password is > 8 chars
    if len(data['password']) < 8:
        flag = True
        flash("Input a valid password. 8 char min.")
    #pw_confirm != password
    if data['pw_confirm'] != data['password']:
        flag = True
        flash("Password does not match")
    # IF flagged, don't insert
    if flag:
        session['data'] = data
        return redirect('/')
    else:
        #SELECT TO check if email is present
        dup_query = "SELECT id from users WHERE email= :email"
        # input_IDs = mysql.query_db(dub_query, data)
        # print input_IDs
        if mysql.query_db(dup_query, data): #Duplicate Check
            flash("This email is already in the our system")
            return redirect('/')
        else:
            #i_query to insert information into database:
            query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (:first_name,:last_name,:email,:password,NOW(),NOW())"
            added = mysql.query_db(query, data)
            if added:
                flash("User Added! Please login now.")
            else:
                flash("User not added, but validation passed")
            return redirect('/')


@app.route('/wall/<user_id>')
def wall(user_id):
    query = "SELECT first_name from users WHERE id= :id"
    data = {'id': user_id,}
    logins = mysql.query_db(query, data)
    return render_template('wall.html',user=logins[0])

app.run(debug=True)
