# examples/env_vars.py
from crono import Crono

crono = Crono()

@crono.every(minutes=15, args=('UTC Time',), env={'TZ': 'UTC'})
def print_time(label):
    import datetime
    print(f"{label}: {datetime.datetime.now()}")

@crono.daily(env={'DEBUG': '1'})
def debug_task():
    print("Debug task running")

if __name__ == "__main__":
    print_time("UTC Time")  # Test with env locally
    crono.write_crontab(filename="env_crontab")