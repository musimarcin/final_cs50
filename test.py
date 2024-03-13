import calendar
from datetime import datetime


cal=calendar

for i in range(len(cal.monthcalendar(2024, 2))):
    for j in range(len(cal.monthcalendar(2024, 2)[i])):
        if cal.monthcalendar(2024, 2)[i][j] == 0:
            print(" ")
        else:
            print(cal.monthcalendar(2024, 2)[i][j])

datem = calendar.month_name[1]
print(datem)
"""
    for j in cal.monthcalendar(2024, 2):
        if cal.monthcalendar(2024, 2)[i][j] != 0:
            print(j)
"""
"""
        <div class="col">Tuesday</div>
        <div class="col">Wednesday</div>
        <div class="col">Thursday</div>
        <div class="col">Friday</div>
        <div class="col">Saturday</div>
        <div class="col">Sunday</div>

        current_month = "December"

for i in range(len(calendar.month_name)):
    if calendar.month_name[i] == current_month:
       print(i)

CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)

CREATE TABLE history (user_id INTEGER NOT NULL, description TEXT NOT NULL, date TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id));

CREATE TABLE events (user_id INTEGER NOT NULL, description TEXT NOT NULL, date TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id));

if date > datetime.now():
    print("kokson")
"""

datey = datetime.now().year + 1


print(datey)

now = datetime.now()

parse = datetime.strptime("2025-02-27T21:33", '%Y-%m-%dT%H:%M')

if now > parse:
    print("kok")
else:
    print("nonkoks")