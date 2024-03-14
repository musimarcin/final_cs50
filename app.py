import os
import calendar
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from functools import wraps

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///database.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            flash("must provide username")
            return render_template("login.html")

        elif not request.form.get("password"):
            flash("must provide password")
            return render_template("login.html")
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]
        
        flash("successfully logged in")
        return redirect("/")
    
    else:
        return render_template("login.html")

    
@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()
    name = request.form.get("username")
    pwd = request.form.get("password")
    pwd2 = request.form.get("confirmation")
    if request.method == "POST":
        if not name:
            flash("must provide username")
            return render_template("register.html")
        elif not pwd:
            flash("must provide password")
            return render_template("register.html")
        elif not pwd2:
            flash("must repeat a password")
            return render_template("register.html")
        elif str(pwd) != str(pwd2):
            flash("passwords does not match")
            return render_template("register.html")
        else:
            rows = db.execute("SELECT * FROM users WHERE username = ?", name)
            if len(rows) > 0:
                flash("user already exists")
                return render_template("register.html")
            else:
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, generate_password_hash(pwd, method='pbkdf2', salt_length=16))
                flash("successfully registered")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def start():

    datem = datetime.now().month
    datew = calendar.day_abbr
    datey = datetime.now().year
    month = calendar.month_name[datem]
    cal = calendar.monthcalendar(datey, datem)
    current_year = request.form.get("current_year", type=int)
    if not current_year:
        datey = datetime.now().year
    else: 
        datey = current_year

    if request.method == "POST":
        current_month = request.form.get("current_month").capitalize()
        current_year = request.form.get("current_year", type=int)
        for i in range(len(calendar.month_name)):
            if calendar.month_name[i] == current_month:
                if request.form["change"] == "prev" and i > 1:
                    datem = i - 1
                elif request.form["change"] == "next" and i < 12:
                    datem = i + 1
                elif request.form["change"] == "prev" and i == 1:
                    datem = 12
                    current_year -= 1
                    datey = current_year
                elif request.form["change"] == "next" and i == 12:
                    datem = 1
                    current_year += 1
                    datey = current_year
        
        month = calendar.month_name[datem]
        cal = calendar.monthcalendar(datey, datem)
        return render_template("index.html", cal=cal, month=month, datew=datew, datey=datey)
    else:
        return render_template("index.html", cal=cal, month=month, datew=datew, datey=datey)
    

@app.route("/add", methods=['GET', 'POST'])
@login_required
def add():

    title = request.form.get("title")
    desc = request.form.get("description")
    date = request.form.get("date")

    if request.method == "POST":
        dateparsed = datetime.strptime(str(date), '%Y-%m-%dT%H:%M')
        if not title:
            flash("must provide title")
            return render_template("add.html")
        elif not desc:
            flash("must provide description")
            return render_template("add.html")
        elif not date or (dateparsed < datetime.now()):
            flash("must provide a valid date")
            return render_template("add.html")
        else:
            db.execute("INSERT INTO events (user_id, description, date, title) VALUES (?, ?, ?, ?)", session["user_id"], desc, date, title)
            db.execute("INSERT INTO history (user_id, description, date, title) VALUES (?, ?, ?, ?)", session["user_id"], desc, date, title)
            flash("successfully added event")
            return render_template("add.html")
    else:
        return render_template("add.html")

@app.route("/list", methods=['GET', 'POST'])
@login_required
def list():
    datenow = datetime.now().strftime("%Y-%m-%dT%H:%M")
    rows = db.execute("SELECT * FROM events WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        fdate = request.form.get("fromdate")
        tdate = request.form.get("todate")
        if fdate == "" and tdate == "":
            fromdate = "1970-01-01T00:00"
            todate = "9999-12-31T23:59" 
        elif fdate == "":
            fromdate = "9999-12-31T23:59"
        elif tdate == "":
            todate = "9999-12-31T23:59"      
        else:
            fromdate = datetime.strptime(str(fdate), '%Y-%m-%dT%H:%M')
            todate = datetime.strptime(str(tdate), '%Y-%m-%dT%H:%M')
        title = request.form.get("title")
        desc = request.form.get("description")
        rows = db.execute("SELECT * FROM events WHERE title LIKE ? AND description LIKE ? AND date >= ? AND date <= ? AND user_id = ?", "%" + title + "%", "%" + desc + "%", fromdate, todate, session["user_id"])        
        return render_template("list.html", datenow=datenow, rows=rows)
    else:

        return render_template("list.html", datenow=datenow, rows=rows)
    
@app.template_filter()
def format_datetime(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M")

@app.route("/edit", methods=['POST'])
def edit():
    id = request.form['edit_btn']
    row = db.execute("SELECT * FROM events WHERE id = ?", id)[0]
    return render_template("edit.html", id=id, row=row)

@app.route("/editevent", methods=['POST'])
def editevent():
    id = request.form['edit_id']
    title = request.form.get("title")
    desc = request.form.get("description")
    date = request.form.get("date")
    db.execute("UPDATE events SET title = ?, description = ?, date = ? WHERE id = ?", title, desc, date, id)
    return redirect("/list")

@app.route("/delete", methods=['POST'])
def delete():
    id = request.form['del_btn']
    db.execute("DELETE FROM events WHERE id = ?", id)
    return redirect("/list")

if __name__ == "__main__":
    app.run(debug=True)