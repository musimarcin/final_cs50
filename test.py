import calendar
from datetime import datetime


cal=calendar

for i in range(len(cal.monthcalendar(2024, 2))):
    for j in range(len(cal.monthcalendar(2024, 2)[i])):
        if cal.monthcalendar(2024, 2)[i][j] == 0:
            print(" ")
        else:
            print(cal.monthcalendar(2024, 2)[i][j])

datem = calendar.month_name[2]
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
"""

datew = calendar.day_name


for i in range(len(datew)):
    print(datew[i])