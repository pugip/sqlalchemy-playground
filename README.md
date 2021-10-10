# sqlalchemy-playground

# Requirements

- If not using `pip` to install, install [Poetry](https://python-poetry.org/docs/#installation)

- Install [Docker Desktop](https://www.docker.com/get-started)

# Installs dependencies

## Poetry

```commandline
poetry install
```

After installing, to find where your new virtualenv is located:
```commandline
poetry env info -p
```

And to enter a shell with the virtualenv:
```commandline
poetry shell
```


## Pip

```commandline
pip install -r requirements.txt
```

# Running

## DB (Postgres)

To start the DB:
```commandline
docker-compose up db
```

To shutdown the DB:
```commandline
docker-compose down
```

## Playground files

```commandline
python examples/<file>.py
```
For example:
```commandline
python examples/constraints.py
```
