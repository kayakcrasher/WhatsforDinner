"""What's for Dinner - FastAPI app."""

import json
import random
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE = Path(__file__).parent
STATIC = BASE / "static"

app = FastAPI(title="What's for Dinner")

RECIPES = json.loads((BASE / "recipes.json").read_text())


# --- Dietary classification ---

MEAT_WORDS = {
    "chicken", "beef", "pork", "lamb", "shrimp", "prawn", "fish", "salmon",
    "tuna", "cod", "halibut", "trout", "tilapia", "catfish", "bacon",
    "sausage", "ham", "turkey", "anchovy", "anchovies", "clam", "clams",
    "guanciale", "prosciutto", "chorizo", "andouille", "kielbasa",
    "pepperoni", "salami", "brisket", "ribeye", "steak", "ribs", "liver",
    "duck", "veal", "crab", "lobster", "scallop", "squid", "octopus",
    "mussels", "oyster", "sardine", "goat", "venison", "rabbit", "quail",
    "pheasant", "meat", "gelatin",
}


def is_vegetarian(recipe):
    """True if no ingredient matches a meat keyword."""
    blob = " ".join(recipe["ingredients"]).lower()
    return not any(word in blob for word in MEAT_WORDS)


def has_peanuts(recipe):
    """True if any ingredient mentions peanuts."""
    blob = " ".join(recipe["ingredients"]).lower()
    return "peanut" in blob


def is_premium(recipe):
    return bool(recipe.get("premium"))


def filter_recipes(recipes, vegetarian=False, no_peanuts=False, tier="free",
                   meal_type=None, protein=None):
    """Apply all filters."""
    out = recipes
    if vegetarian:
        out = [r for r in out if is_vegetarian(r)]
    if no_peanuts:
        out = [r for r in out if not has_peanuts(r)]
    if tier != "paid":
        out = [r for r in out if not is_premium(r)]
    if meal_type and meal_type != "all":
        out = [r for r in out if r.get("meal_type") == meal_type]
    if protein and protein != "any":
        out = [r for r in out if r.get("protein") == protein]
    return out


# --- Routes ---

@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/recipes")
def list_recipes(vegetarian: bool = False, no_peanuts: bool = False, tier: str = "free",
                 meal_type: str | None = None, protein: str | None = None):
    filtered = filter_recipes(RECIPES, vegetarian, no_peanuts, tier, meal_type, protein)
    return {
        "count": len(filtered),
        "total": len(RECIPES),
        "tier": tier,
        "recipes": filtered,
    }


@app.get("/api/spin")
def spin(vegetarian: bool = False, no_peanuts: bool = False, tier: str = "free",
         meal_type: str | None = None, protein: str | None = None):
    filtered = filter_recipes(RECIPES, vegetarian, no_peanuts, tier, meal_type, protein)
    if not filtered:
        raise HTTPException(404, "No recipes match your filters")
    return random.choice(filtered)


app.mount("/static", StaticFiles(directory=STATIC), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
