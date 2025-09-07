from flask import *
import sqlite3
import secrets
import time
import os
import base64

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

command = '''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT NOT NULL,
            location TEXT NOT NULL
        );
    '''
cursor.execute(command)

command = '''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            before_image TEXT NOT NULL,
            after_image TEXT NOT NULL,
            location TEXT NOT NULL
        );
    '''
cursor.execute(command)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()

    cursor.execute("select * from records")
    result = cursor.fetchall()
    return render_template('index.html', result=result)

@app.route('/adminhome')
def adminhome():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()

    cursor.execute("select * from items")
    result = cursor.fetchall()
    return render_template('adminlog.html', result=result)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        email = request.form['email']
        password = request.form['password']

        query = "SELECT * FROM user WHERE email = '"+email+"' AND password= '"+password+"'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            session['phone'] = result[2]
            return render_template('userlog.html')
        else:
            return render_template('signin.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('signin.html', msg='Successfully Registered')
    
    return render_template('signup.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        print(email, password)

        if email == 'deepakgowdadeepu36@gmail.com' and password == 'Deepak@123':
            return redirect(url_for('adminhome'))
        else:
            return render_template('admin.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('admin.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        image = request.files['image']
        loc = request.form['loc']

        file_content = image.read()
        my_string = base64.b64encode(file_content).decode('utf-8')

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        cursor.execute("insert into items values (NULL, ?,?)", [my_string, loc])
        connection.commit()

        return render_template('userlog.html')
    return render_template('userlog.html')


@app.route('/updates', methods=['GET', 'POST'])
def updates():
    if request.method == 'POST':
        before = request.files['before']
        after = request.files['after']
        loc = request.form['loc']

        before_content = before.read()
        before_string = base64.b64encode(before_content).decode('utf-8')

        after_content = after.read()
        after_string = base64.b64encode(after_content).decode('utf-8')

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        cursor.execute("insert into records values (NULL, ?,?,?)", [before_string, after_string, loc])
        connection.commit()

        return render_template('updates.html')
    return render_template('updates.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
