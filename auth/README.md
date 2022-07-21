# The authentication service

This module is written in python and uses the FastAPI package.

To start the server, first install Python 3 (if not already installed) and the
pip package manager, and then install the FastAPI package :

```bash
sudo apt install python3 python3-pip # use whatever package manager your distribution provides
pip install "fastapi[all]"
pip install "uvicorn[all]" # the cli tool to start the project
```

**WARNING** : you might get some warnings saying that `~/.local/bin` is not in
the `PATH` variable. If this is the case, make sure to add the direcrory to the
`PATH` variable.

After successfully installing the dependencies, run :

```bash
uvicorn main:app --reload
```

The server should start.

You can find more documentation [over here](https://fastapi.tiangolo.com/tutorial/).
