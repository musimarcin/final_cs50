import os
import calendar
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def start():
    session.clear()
    datew = calendar.day_name
    datey = datetime.now().year
    datem = datetime.now().month
    month = calendar.month_name[datem]
    cal = calendar.monthcalendar(datey, datem)

    return render_template("index.html", cal=cal, month=month, datew=datew)


@app.route("/change", methods=["GET", "POST"])
def changep():
    if request.method == "POST":
        datem = datetime.now().month
        datew = calendar.day_name
        datey = datetime.now().year
        current_month = request.form.get("current_month").capitalize()
        for i in range(len(calendar.month_name)):
            if calendar.month_name[i] == current_month:
                if request.form["change"] == "prev" and i > 1:
                    datem = i - 1
                elif request.form["change"] == "next" and i < 12:
                    datem = i + 1
                else:
                    return ('', 204)

        month = calendar.month_name[datem]
        cal = calendar.monthcalendar(datey, datem)
        return render_template("index.html", cal=cal, month=month, datew=datew)
    