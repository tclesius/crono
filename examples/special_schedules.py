# examples/special_schedules.py
from crono import Crono

crono = Crono()

@crono.reboot(args=('Booted',))
def on_reboot(message):
    print(f"System says: {message}")

@crono.hourly()
def hourly_check():
    print("Hourly system check")

@crono.daily()
def daily_report():
    print("Daily report generated")

@crono.weekly()
def weekly_cleanup():
    print("Weekly cleanup done")

@crono.monthly()
def monthly_summary():
    print("Monthly summary printed")

@crono.yearly()
def yearly_review():
    print("Yearly review completed")

if __name__ == "__main__":
    on_reboot("Booted")  # Test one directly
    crono.write_crontab(filename="special_crontab")