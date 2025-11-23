from flask import Flask,request,redirect,flash,render_template,session
import sqlite3
import re

app = Flask(__name__)
app.secret_key = "demo_secret"


# implementaion of sqlite3
database = "users.db"
def activateingDB():
    connecting = sqlite3.connect(database)
    X = connecting.cursor()
    X.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)")
    connecting.commit()
    connecting.close()
activateingDB()

#get user detalk iif exists
def user_details(email):
    email = email.strip().lower()
    connectecting = sqlite3.connect(database)
    Y = connectecting.cursor()
    Y.execute("SELECT email,password FROM users WHERE email=?",(email,))
    row= Y.fetchone()
    Y.close()
    return row

# create user if not exist
def create_user(email, password):
    email = email.strip().lower()
    conn = sqlite3.connect(database)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?,?)",(email,password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

  
@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    row = user_details(email)
    if not row:
        flash("you dont have account")
        return redirect("/signup")

    if password == row[1]:
        session["user"] = email
        return redirect("/dashboard")
    else:
        flash("Wrong passcode")
        return redirect("/login")

@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    password2 = request.form["password2"]

    if password != password2:
        flash("wrong pass")
        return redirect("/signup")

    if create_user(email, password):
        flash("Account created login")
        return redirect("/login")
    else:
        flash("User already exists.")
        return redirect("/login")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", email=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug = True)