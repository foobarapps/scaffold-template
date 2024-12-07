# {{ cookiecutter.project_name }}

## First-time setup

The following steps need to be done only once when first setting up the app.

### Prerequisites

* Git
* `pre-commit`
* `cruft`
* Docker Compose

### Set up pre-commit hooks

```shell
pre-commit install
```

### Add a `.env` file

Create an empty `.env` file and add the following variables:

```shell
DOMAIN=app.localhost
DATABASE_URL=postgresql://user:password@db/development
MAIL_HOSTNAME=mailhog
MAIL_PORT=1025
MAIL_DEFAULT_SENDER="Your Company <info@yourcompany.com>"
```

Then, generate a secret key and add it to the file as SECRET_KEY variable:

```shell
docker compose run app uv run python -c 'import secrets; print(secrets.token_hex())'
```

### Upgrade dependencies

```shell
docker compose run app uv lock --upgrade
```

## Running the app

```shell
docker compose up
```

## Cookbook

### Running linters, formatters, type checkers, etc.

```shell
pre-commit run --all-files
```

### Adding dependencies

```shell
docker compose run app uv add ...
```

### Generating a database migration

```shell
docker compose run app uv run alembic revision --autogenerate -m "Message"
docker compose run app uv run alembic upgrade head
```

### Running tests

```shell
docker compose run app pytest
```
