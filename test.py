import calendar
from datetime import datetime
from cs50 import SQL
db = SQL("sqlite:///database.db")

datem = datetime.now().month-1
datey = datetime.now().year
print(datem)
if datem < 10:
    todatem=datem+2
    datemdb="0"+str(datem)
    if todatem < 10:
        todatemdb = "0" + str(todatem)
    else:
        todatemdb=todatem
rows = db.execute("SELECT * FROM events WHERE date > ? AND date < ?", str(datey)+"-"+datemdb, str(datey)+"-"+todatemdb)
table_days = {}

for row in range(len(rows)):
    q = rows[row]['date']
    theday = datetime.strptime(q, '%Y-%m-%dT%H:%M').day
    if theday in table_days:
        if not isinstance(table_days[theday], list):
            table_days[theday] = [table_days[theday]]
        table_days[theday].append(rows[row]['title'])
    else: 
        table_days[theday] = rows[row]['title']

cal=calendar

calnow=cal.monthcalendar(datey,datetime.now().month)

for i in range(len(calnow)):
    for j in range(len(calnow[i])):
        if calnow[i][j] == 0:
            #print(" ")
            pass
        else:
            #print(calnow[i][j])
            for k in table_days:
                if calnow[i][j] == k:
                    pass
                    #print(table_days[k])

print(rows)
print(table_days)

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

CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE history (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, title TEXT NOT NULL, description TEXT NOT NULL, date TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, action TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, title TEXT NOT NULL, description TEXT NOT NULL, date TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id));

if date > datetime.now():
    print("kokson")
"""


