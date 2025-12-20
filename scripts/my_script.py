import datetime

with open("/data/cron.log", "a") as f:
    f.write(f"Cron ran at {datetime.datetime.now()}\n")
