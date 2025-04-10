# examples/disable_jobs.py
from crono import Crono

crono = Crono()

@crono.every(minutes=5, args=('Active',))
def active_task(message):
    print(f"This is {message}")

@crono.every(minutes=10, args=('Inactive',), enabled=False)
def inactive_task(message):
    print(f"This is {message} - should not run")

@crono.reboot(enabled=False)
def disabled_reboot():
    print("Disabled reboot task")

if __name__ == "__main__":
    active_task("Active")  # Test active task
    crono.write_crontab(filename="disable_crontab")