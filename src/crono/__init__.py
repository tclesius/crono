# src/crono/__init__.py
import sys
from crontab import CronTab
from pathlib import Path
import inspect

class Crono:
    def __init__(self):
        """Initialize Crono with the current Python executable."""
        self.jobs = []
        self.python_exec = sys.executable

    def _get_target(self, func):
        """Get module:function or file:function string for the runner."""
        module = inspect.getmodule(func)
        if module.__name__ != '__main__':
            return f"{module.__name__}:{func.__name__}"
        file_path = Path(inspect.getfile(func)).absolute()
        return f"{file_path}:{func.__name__}"

    def every(self, minutes=None, hours=None, days=None, args=(), env=None, enabled=True):
        """Schedule a function to run periodically with optional args, env, and enabled state."""
        def decorator(func):
            params = {'minutes': minutes, 'hours': hours, 'days': days}
            schedule = {k: v for k, v in params.items() if v is not None}
            if not schedule:
                raise ValueError("`every` needs at least one time unit.")
            self.jobs.append({
                'target': self._get_target(func),
                'type': 'every',
                'params': schedule,
                'args': args,
                'env': env or {},
                'enabled': enabled
            })
            return func
        return decorator

    def at(self, minute, hour=None, day_of_month=None, month=None, day_of_week=None, args=(), env=None, enabled=True):
        """Schedule a function at specific times with optional args, env, and enabled state."""
        def decorator(func):
            cron = f"{minute} {hour or '*'} {day_of_month or '*'} {month or '*'} {day_of_week or '*'}"
            self.jobs.append({
                'target': self._get_target(func),
                'type': 'expr',
                'params': {'expression': cron},
                'args': args,
                'env': env or {},
                'enabled': enabled
            })
            return func
        return decorator

    def expr(self, expression, args=(), env=None, enabled=True):
        """Schedule a function with a raw cron expression and optional args, env, and enabled state."""
        def decorator(func):
            self.jobs.append({
                'target': self._get_target(func),
                'type': 'expr',
                'params': {'expression': expression},
                'args': args,
                'env': env or {},
                'enabled': enabled
            })
            return func
        return decorator

    def reboot(self, args=(), env=None, enabled=True):
        """Schedule a function to run once at system reboot with optional args, env, and enabled state."""
        def decorator(func):
            self.jobs.append({
                'target': self._get_target(func),
                'type': 'reboot',
                'params': {'expression': '@reboot'},
                'args': args,
                'env': env or {},
                'enabled': enabled
            })
            return func
        return decorator

    def hourly(self, args=(), env=None, enabled=True):
        """Schedule a function to run hourly with optional args, env, and enabled state."""
        def decorator(func):
            self.jobs.append({
                'target': self._get_target(func),
                'type': 'expr',
                'params': {'expression': '@hourly'},
                'args': args,
                'env': env or {},
                'enabled': enabled
            })
            return func
        return decorator

    def daily(self, args=(), env=None, enabled=True):
        """Schedule a function to run daily with optional args, env, and enabled state."""
        def decorator(func):
            self.jobs.append({
                'target': self._get_target(func),
                'type': 'expr',
                'params': {'expression': '@daily'},
                'args': args,
                'env': env or {},
                'enabled': enabled
            })
            return func
        return decorator

    def weekly(self, args=(), env=None, enabled=True):
        """Schedule a function to run weekly with optional args, env, and enabled state."""
        def decorator(func):
            self.jobs.append({
                'target': self._get_target(func),
                'type': 'expr',
                'params': {'expression': '@weekly'},
                'args': args,
                'env': env or {},
                'enabled': enabled
            })
            return func
        return decorator

    def monthly(self, args=(), env=None, enabled=True):
        """Schedule a function to run monthly with optional args, env, and enabled state."""
        def decorator(func):
            self.jobs.append({
                'target': self._get_target(func),
                'type': 'expr',
                'params': {'expression': '@monthly'},
                'args': args,
                'env': env or {},
                'enabled': enabled
            })
            return func
        return decorator

    def yearly(self, args=(), env=None, enabled=True):
        """Schedule a function to run yearly with optional args, env, and enabled state."""
        def decorator(func):
            self.jobs.append({
                'target': self._get_target(func),
                'type': 'expr',
                'params': {'expression': '@yearly'},
                'args': args,
                'env': env or {},
                'enabled': enabled
            })
            return func
        return decorator

    def write_crontab(self, use_user_crontab=False, filename=None):
        """Write jobs to crontab with unique identifiers, validation, env vars, and enabled state."""
        if use_user_crontab:
            cron = CronTab(user=True)
        else:
            filepath = filename or str(Path.home() / ".crono_jobs")
            cron = CronTab(tabfile=filepath)
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        for job in self.jobs:
            command = f"{self.python_exec} -m crono.runner {job['target']} {' '.join(map(str, job.get('args', [])))}"
            comment = f"crono:{job['target']}"
            # Remove existing job with same comment
            existing = list(cron.find_comment(comment))
            if existing:
                cron.remove(existing[0])
            cron_job = cron.new(command=command, comment=comment)
            # Set environment variables
            for key, value in job.get('env', {}).items():
                cron_job.env[key] = str(value)
            # Set schedule
            if job['type'] == 'every':
                params = job['params']
                if 'minutes' in params:
                    cron_job.minute.every(params['minutes'])
                elif 'hours' in params:
                    cron_job.hour.every(params['hours'])
                elif 'days' in params:
                    cron_job.day.every(params['days'])
            elif job['type'] in ('expr', 'reboot'):
                cron_job.setall(job['params']['expression'])
            # Validate job
            if not cron_job.is_valid():
                print(f"Skipping invalid job: {command}", file=sys.stderr)
                cron.remove(cron_job)
                continue
            # Enable/disable job
            cron_job.enable(job.get('enabled', True))

        cron.write()