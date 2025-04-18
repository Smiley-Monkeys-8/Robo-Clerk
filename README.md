# Robo-Clerk

<img title="a title" alt="Alt text" src="docs/RoboClerk.png">


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
SAMBANOVA_API_KEY=<sambanova api key>
API_URL=https://hackathon-api.mlo.sehlat.io/game
```

For using LLM to extract semantic data from text summaries a https://sambanova.ai/ API and add the access token to the `.env`

For regex matching extraction use the TXTProcessor instead of TXTProcessorSambanova in `doc_master.py`

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


# Web App

## Setup

Download the processed data set: https://drive.google.com/file/d/13mGcHNlrvIvREmcxHrOpI5y46qCotzZQ/view?usp=drive_link

And place it in "out" folder top of the project

---
Alternatively run the processor `poetry run robo-processor`

## Frontend

```
cd frontend
npm install
npm run dev
```

## Backend

```
poetry run robo-server
```

# Team

This was developed as part of [SwissHacks 2025](https://www.swisshacks.com/) for the JB challenge.

Members of **Smiling Monkeys** team:

|   **[Margarita Ferreira](https://www.linkedin.com/in/margarita-ferreira/)**  | **[Marisa Davis](https://www.linkedin.com/in/marisa-j-davis/)** | **[Valdilene Siqueira](https://www.linkedin.com/in/valdilenesiqueira/)** | **[Alexandru But](https://www.linkedin.com/in/alexandrubut/)**   |
|---|---|---|---|




