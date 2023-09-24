from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import base64
# from flask_session import Session
import pymysql
import hashlib
import binascii
import json
from functools import wraps
salt = "cpe334"

app = Flask(__name__)
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='stock'
)
cur = conn.cursor()
app.secret_key = "super secret key"

# function login
@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        dataBase_password = password + salt
        hashed = hashlib.md5(dataBase_password.encode())
        
        cur.execute("SELECT * FROM User_List WHERE Username = %s AND Password = %s",
                    (username, hashed.hexdigest(),))
        
        record = cur.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            print('1111')
            return redirect(url_for('staff'))
        else:
            msg = "Incorrect"

        conn.commit()
    return render_template('login.html', msg=msg)


def islogin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session or not session['loggedin']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    conn.ping(reconnect=True)
    msg = '' 
    return render_template('login.html', msg=msg)

# function logout
@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('home'))



if __name__ == '__main__':
       app.run(debug=True)



    
