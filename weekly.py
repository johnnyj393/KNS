# The only option on pythonanywhere is to run daily, so this will be run every day but the main.py will only be run
# every Monday.

import datetime
from main import master_generate

today = datetime.date.today()
weekday = today.weekday()

if weekday == 0:
    master_generate()
