# Crono

Crono is a lightweight Python library for scheduling tasks using cron, built on top of `python-crontab`✨. It provides a decorator-based API to easily schedule both synchronous and asynchronous functions with support for arguments, environment variables, and special cron schedules like `@reboot` or `@hourly`.

## Features
- Schedule tasks with decorators: `every`, `at`, `expr`, `reboot`, `hourly`, `daily`, `weekly`, `monthly`, `yearly`.
- Supports both sync and async functions via a simple runner.
- Pass arguments and environment variables to scheduled tasks.
- Enable/disable jobs without removing them.
- Write jobs to user crontab or a file.
- Minimal dependencies: only `python-crontab`.

## Installation
Install Crono using pip or your preferred package manager:

```bash
pip install crono
```

Clone this repository and place \`crono/\` in your project directory, or install it as a local package:

```bash
git clone https://github.com/yourusername/crono.git
cd crono
pip install -e .
```

## Usage
Define tasks with decorators and write them to a crontab:

```python
from crono import Crono

crono = Crono()

@crono.every(minutes=5, args=('Alice',))
def greet(name):
    print(f"Hello, {name}!")

@crono.reboot(args=('Startup',))
async def on_boot(message):
    await asyncio.sleep(1)
    print(f"System started: {message}")

if __name__ == "__main__":
    crono.write_crontab(filename="my_crontab")
```

Run your script to generate the crontab file, then load it into your system cron:

```bash
crontab my_crontab
```

### Key Decorators
- `@crono.every(minutes=n, hours=n, days=n, args=(), env={}, enabled=True)`: Run periodically.
- `@crono.at(minute, hour, day_of_month, month, day_of_week, args=(), env={}, enabled=True)`: Run at specific times.
- `@crono.expr("cron expression", args=(), env={}, enabled=True)`: Use a raw cron expression.
- `@crono.reboot(args=(), env={}, enabled=True)`: Run at system reboot.
- `@crono.hourly(args=(), env={}, enabled=True)`: Run every hour (also `@daily`, `@weekly`, `@monthly`, `@yearly`).

### Running Directly
Test tasks directly (sync tasks run immediately, async tasks need `asyncio.run`):

```python
greet("Alice")  # Outputs: Hello, Alice!
asyncio.run(on_boot("Test"))  # Outputs: System started: Test (after 1s)
```

## Examples
See the `examples/` directory for practical use cases:
- `basic.py`: Simple sync and async tasks.
- `special_schedules.py`: Using `@reboot`, `@hourly`, etc.
- `env_vars.py`: Setting environment variables.
- `disable_jobs.py`: Disabling specific jobs.

Run examples with:

```bash
python examples/basic.py
```

## Notes
- Ensure your Python executable (`sys.executable`) is accessible to cron.
- Async tasks require the `runner.py` script to handle `asyncio.run`.
- Invalid cron jobs are skipped with a warning to `stderr`.

## Contributing
Feel free to open issues or PRs on GitHub!.

## License
MIT License - see `LICENSE` for details.
