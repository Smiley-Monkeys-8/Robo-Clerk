# Robo-Clerk

**Robo Clerk** is a Relationship Manager assistant for reviewing customer documents.

* It checks if the information is complete and consistent.
* If something is missing or wrong, **it flags** the issue.
* It also **explains** why a customer is rejected.
* No customer data is sent to third parties unless anonymized.

Read more in [About](docs/About.md)

## Getting Started

### Setup ENV

in `.env` file put the variables:

```sh
API_KEY=<your_api_key>
API_URL=https://hackathon-api.mlo.sehlat.io/game
```

### Setup Poetry

#### Install Poetry
* install pipx: https://pipx.pypa.io/stable/installation/
* install poetry: `pipx install poetry`

#### Install Dependencies

* `tesseract-ocr`

Ubuntu:
```
sudo apt install tesseract-ocr
```

MAC:
```
brew install tesseract
```

#### Init Project
```
poetry shell
poetry install
```

### Run App

```
poetry run robo-clerk
```

