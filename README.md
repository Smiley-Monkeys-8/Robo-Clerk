# Robo-Clerk

## Getting Started

### Virtual Environment

```sh
python3 -m venv .venv
# source env
. .venv
pip install -r requirements.txt
```

### Setup ENV

in `.env` file put the variables:

API_KEY: `your_api_key`
API_URL: https://hackathon-api.mlo.sehlat.io/

### Setup Poetry

```
curl -sSL https://install.python-poetry.org | python3 -
poetry shell
poetry install
```

### Run App

```
poetry run robo-clerk
```