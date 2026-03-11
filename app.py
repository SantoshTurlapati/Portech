from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "portech_secret"

# Create Database
def create_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    business TEXT,
    type TEXT,
    requirements TEXT
    )
    ''')

    conn.commit()
    conn.close()

create_db()

# LOGIN PAGE
@app.route('/')
def login():
    return render_template("login.html")


# LOGIN CHECK
@app.route('/login', methods=['POST'])
def login_check():

    username=request.form['username']
    password=request.form['password']

    conn=sqlite3.connect('database.db')
    c=conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))

    user=c.fetchone()

    conn.close()

    if user:
        session['user']=username
        return redirect('/home')

    else:
        return "Invalid Login"



# REGISTER PAGE
@app.route('/register')
def register():
    return render_template("register.html")


# REGISTER SAVE
@app.route('/registersave',methods=['POST'])
def registersave():

    username=request.form['username']
    password=request.form['password']

    conn=sqlite3.connect('database.db')
    c=conn.cursor()

    c.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))

    conn.commit()
    conn.close()

    return redirect('/')



# HOME PAGE
@app.route('/home')
def home():

    if 'user' in session:
        return render_template("home.html")

    else:
        return redirect('/')


# GET STARTED PAGE
@app.route('/getstarted')
def getstarted():

    if 'user' in session:
        return render_template("getstarted.html")

    else:
        return redirect('/')


# SAVE PROJECT
@app.route('/saveproject',methods=['POST'])
def saveproject():

    name=request.form['name']
    email=request.form['email']
    business=request.form['business']
    type=request.form['type']
    requirements=request.form['requirements']

    conn=sqlite3.connect('database.db')
    c=conn.cursor()

    c.execute("INSERT INTO projects(name,email,business,type,requirements) VALUES(?,?,?,?,?)",
              (name,email,business,type,requirements))

    conn.commit()
    conn.close()

    return "Project Saved Successfully"



# LOGOUT
@app.route('/logout')
def logout():

    session.pop('user',None)

    return redirect('/')


app.run(debug=True)