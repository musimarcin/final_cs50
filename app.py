import os
import calendar
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'example@gmail.com'
app.config['MAIL_PASSWORD'] = '***'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['TESTING'] = False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_DEBUG'] = True
mail = Mail(app) 
db = SQL("sqlite:///database.db")



def login_required(f):
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
    email = request.form.get("email")
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
        elif not email:
            flash("must provide an e-mail")
            return render_template("register.html")
        else:
            rows = db.execute("SELECT * FROM users WHERE username = ? OR email = ?", name, email)
            if len(rows) > 0:
                flash("user or email already exists")
                return render_template("register.html")
            else:                
                msg = Message("Thank you for registering ", sender="example@gmail.com", recipients=[email])
                msg.body = 'Hello Flask message sent from Flask-Mail'
                mail.send(msg)
                db.execute("INSERT INTO users (username, hash, email) VALUES(?, ?, ?)", name, generate_password_hash(pwd, method='pbkdf2', salt_length=16), email)
                flash("successfully registered")
                return redirect("/")
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("successfully logged out")
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def start():
    datem = datetime.now().month
    datew = calendar.day_abbr
    datey = datetime.now().year
    month = calendar.month_name[datem]
    cal = calendar.monthcalendar(datey, datem)
    mainusername = None
    table_days = {}

    if not session.get("user_id") is None:
        mainusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        todatem = datem + 1
        
        if datem <= 9:
            datemdb = "0" + str(datem)
        else:
            datemdb = str(datem)
        
        if todatem <= 9:
            todatemdb = "0" + str(todatem)
        else:
            todatemdb = str(todatem)

        rows = db.execute("SELECT * FROM events WHERE date > ? AND date < ? AND user_id = ?", str(datey)+"-"+datemdb, str(datey)+"-"+todatemdb, session["user_id"])
        for row in range(len(rows)):
            q = rows[row]['date']
            theday = datetime.strptime(q, '%Y-%m-%dT%H:%M').day
            if theday in table_days:
                if not isinstance(table_days[theday], type([])):
                    table_days[theday] = [table_days[theday]]
                table_days[theday].append(rows[row]['title'])
            else: 
                table_days[theday] = rows[row]['title']

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
                elif request.form["change"] == "nextyear":
                    datem = i
                    datey = current_year + 1
                elif request.form["change"] == "prevyear":
                    datem = i
                    datey = current_year - 1

        table_days = {}

        if not session.get("user_id") is None:
            mainusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
            todatem = datem + 1

            if datem <= 9:
                datemdb = "0" + str(datem)
            else:
                datemdb = str(datem)
            
            if todatem <= 9:
                todatemdb = "0" + str(todatem)
            else:
                todatemdb = str(todatem)

            rows = db.execute("SELECT * FROM events WHERE date > ? AND date < ? AND user_id = ?", str(datey)+"-"+datemdb, str(datey)+"-"+todatemdb, session["user_id"])           
            for row in range(len(rows)):
                q = rows[row]['date']
                theday = datetime.strptime(q, '%Y-%m-%dT%H:%M').day
                if theday in table_days:
                    if not isinstance(table_days[theday], type([])):
                        table_days[theday] = [table_days[theday]]
                    table_days[theday].append(rows[row]['title'])
                else: 
                    table_days[theday] = rows[row]['title']

        month = calendar.month_name[datem]
        cal = calendar.monthcalendar(datey, datem)
        return render_template("index.html", cal=cal, month=month, datew=datew, datey=datey, table_days=table_days, mainusername=mainusername)
    else:
        return render_template("index.html", cal=cal, month=month, datew=datew, datey=datey, table_days=table_days, mainusername=mainusername)
    

@app.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    mainusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    title = request.form.get("title")
    desc = request.form.get("description")
    date = request.form.get("date")

    if request.method == "POST":
        dateparsed = datetime.strptime(str(date), '%Y-%m-%dT%H:%M')
        if not title:
            flash("must provide title")
            return render_template("add.html", mainusername=mainusername)
        elif not desc:
            flash("must provide description")
            return render_template("add.html", mainusername=mainusername)
        elif not date or (dateparsed < datetime.now()):
            flash("must provide a valid date")
            return render_template("add.html", mainusername=mainusername)
        else:
            db.execute("INSERT INTO events (user_id, title, description, date) VALUES (?, ?, ?, ?)", session["user_id"], title, desc, date)
            db.execute("INSERT INTO history (user_id, title, description, date, action) VALUES (?, ?, ?, ?, ?)", session["user_id"], title, desc, date, "Added")
            flash("successfully added event")
            return render_template("add.html", mainusername=mainusername)
    else:
        return render_template("add.html", mainusername=mainusername)

@app.route("/list", methods=['GET', 'POST'])
@login_required
def list():
    mainusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
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
        return render_template("list.html", datenow=datenow, rows=rows, mainusername=mainusername)
    else:

        return render_template("list.html", datenow=datenow, rows=rows, mainusername=mainusername)
    
@app.template_filter()
def format_datetime(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M")

@app.route("/edit", methods=['POST'])
@login_required
def edit():
    mainusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    id = request.form['edit_btn']
    row = db.execute("SELECT * FROM events WHERE id = ?", id)[0]
    return render_template("edit.html", id=id, row=row, mainusername=mainusername)

@app.route("/editevent", methods=['POST'])
@login_required
def editevent():
    mainusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    id = request.form['edit_id']
    title = request.form.get("title")
    desc = request.form.get("description")
    date = request.form.get("date")

    dateparsed = datetime.strptime(str(date), '%Y-%m-%dT%H:%M')
    if not title:
        flash("must provide title")
        return redirect("/list")
    elif not desc:
        flash("must provide description")
        return redirect("/list")
    elif not date or (dateparsed < datetime.now()):
        flash("must provide a valid date")
        return redirect("/list")
    else:
        db.execute("UPDATE events SET title = ?, description = ?, date = ? WHERE id = ? AND user_id = ?", title, desc, date, id, session["user_id"])
        db.execute("INSERT INTO history (user_id, title, description, date, action) VALUES (?, ?, ?, ?, ?)", session["user_id"], title, desc, date, "Edited")
        flash("successfully edited")
        return redirect("/list")

@app.route("/delete", methods=['POST'])
@login_required
def delete():
    id = request.form['del_btn']
    row = db.execute("SELECT * FROM events WHERE id = ?", id)[0]
    title = row['title']
    desc = row['description']
    date = row['date']
    db.execute("INSERT INTO history (user_id, title, description, date, action) VALUES (?, ?, ?, ?, ?)", session["user_id"], title, desc, date, "Deleted")
    db.execute("DELETE FROM events WHERE id = ?", id)
    flash("successfully deleted")
    return redirect("/list")

@app.route("/history", methods=['GET'])
@login_required
def history():
    mainusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    rows = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])
    return render_template("history.html", rows=rows, mainusername=mainusername)

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    mainusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    if request.method == "POST":
        password = request.form.get("password")
        email = request.form.get("email")
        if request.form["change"] == "email":
            db.execute("UPDATE users SET email = ? WHERE id = ?", email, session["user_id"])
            flash("e-mail changed successfully")
        if request.form["change"] == "password":
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(password, method='pbkdf2', salt_length=16), session["user_id"])
            flash("password changed successfully")
        if request.form["change"] == "delete":
            db.execute("DELETE FROM events WHERE user_id = ?", session["user_id"])
            db.execute("DELETE FROM history WHERE user_id = ?", session["user_id"])
            db.execute("DELETE FROM users WHERE id = ?", session["user_id"])
            flash("user deleted successfully")
            return redirect("/logout")
        emaildb = db.execute("SELECT email FROM users where id = ?", session["user_id"])[0]['email']
        return render_template("settings.html", email=emaildb, mainusername=mainusername)
        
    else:
        email = db.execute("SELECT email FROM users where id = ?", session["user_id"])[0]['email']
        return render_template("settings.html", email=email, mainusername=mainusername)

if __name__ == "__main__":
    app.run(debug=True)