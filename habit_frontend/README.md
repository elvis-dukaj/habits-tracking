# Setting up the CLI

The CLI requires a virtual environment to run:

For Posix-like system:

```commandline
python -m venv .venv
. .venv/bin/activate
pip install .
```

# Running the CLI
Now from inside the virtual environment it's possible to call the `htr` (HabitTRacker) terminal.

```commandline
htr --help
Usage: htr [OPTIONS] COMMAND [ARGS]...

Options:
  --endpoint TEXT  server endpoint
  --help           Show this message and exit.

Commands:
  habit
  streak
  user
```

