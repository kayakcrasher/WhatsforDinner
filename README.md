# What's for Dinner?

An app for people who can't decide what to eat.


## Stack

- FastAPI + Uvicorn
- HTML/CSS/JS frontend
- 165+ recipes with cuisine, meal, protein, and dietary filters
- Free tier + premium ($1.25)

## Development

    python3.12 -m venv ~/kivyenv
    source ~/kivyenv/bin/activate
    pip install -r requirements.txt -r requirements-dev.txt
    python main.py

Open http://localhost:8000

## Tests

    pytest -v

## Attribution

Recipes curated locally and from TheMealDB.
