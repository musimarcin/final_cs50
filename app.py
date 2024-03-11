import os
import calendar
from datetime import datetime

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
connect = sqlite3.connect('database.db')

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
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

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
            return apology("must provide username", 400)
        elif not pwd:
            return apology("must provide password", 400)
        elif not pwd2:
            return apology("must provide password2", 400)
        elif str(pwd) != str(pwd2):
            return apology("passwords does not match", 400)
        else:
            rows = db.execute("SELECT * FROM users WHERE username = ?", name)
            if len(rows) > 0:
                return apology("user already exists", 400)
            else:
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, generate_password_hash(pwd, method='pbkdf2', salt_length=16))
    return render_template("register.html")

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
    

if __name__ == "__main__":
    app.run(debug=True)