# src/crono/runner.py
import importlib
import sys
import asyncio
import inspect

def run_task(target: str, *args):
    """Run a target function specified as 'module:function' with optional args."""
    try:
        module_part, function_name = target.rsplit(':', 1)
        module = importlib.import_module(module_part)
        func = getattr(module, function_name)
        if inspect.iscoroutinefunction(func):
            asyncio.run(func(*args))
        else:
            func(*args)
    except Exception as e:
        print(f"Error running {target}: {e}", file=sys.stderr)

if __name__ == "__main__":
    verbose = '--verbose' in sys.argv
    if verbose:
        sys.argv.remove('--verbose')
    if len(sys.argv) < 2:
        print("Usage: python -m crono.runner <module:function> [args...] [--verbose]", file=sys.stderr)
        sys.exit(1)
    if verbose:
        print(f"Running {sys.argv[1]} with args {sys.argv[2:]}")
    run_task(sys.argv[1], *sys.argv[2:])