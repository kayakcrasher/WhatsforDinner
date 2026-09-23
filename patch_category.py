from pathlib import Path
p = Path("main.py")
s = p.read_text()

# Expand filter_recipes
old = '''def filter_recipes(recipes, vegetarian=False, no_peanuts=False, tier="free",
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
    return out'''

new = '''def filter_recipes(recipes, vegetarian=False, no_peanuts=False, tier="free",
                   meal_type=None, protein=None, category=None):
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
    if category and category != "all":
        out = [r for r in out if (r.get("category") or "").lower() == category.lower()]
    return out'''

s = s.replace(old, new)

# Expand list_recipes signature
s = s.replace(
    'def list_recipes(vegetarian: bool = False, no_peanuts: bool = False, tier: str = "free",\n                 meal_type: str | None = None, protein: str | None = None):\n    filtered = filter_recipes(RECIPES, vegetarian, no_peanuts, tier, meal_type, protein)',
    'def list_recipes(vegetarian: bool = False, no_peanuts: bool = False, tier: str = "free",\n                 meal_type: str | None = None, protein: str | None = None,\n                 category: str | None = None):\n    filtered = filter_recipes(RECIPES, vegetarian, no_peanuts, tier, meal_type, protein, category)'
)

# Expand spin signature
s = s.replace(
    'def spin(vegetarian: bool = False, no_peanuts: bool = False, tier: str = "free",\n         meal_type: str | None = None, protein: str | None = None):\n    filtered = filter_recipes(RECIPES, vegetarian, no_peanuts, tier, meal_type, protein)',
    'def spin(vegetarian: bool = False, no_peanuts: bool = False, tier: str = "free",\n         meal_type: str | None = None, protein: str | None = None,\n         category: str | None = None):\n    filtered = filter_recipes(RECIPES, vegetarian, no_peanuts, tier, meal_type, protein, category)'
)

# Add /api/categories endpoint after list_recipes
needle = 'app.mount("/static", StaticFiles(directory=STATIC), name="static")'
inject = '''@app.get("/api/categories")
def categories(tier: str = "free"):
    """Return list of cuisines with counts, respecting tier."""
    pool = RECIPES if tier == "paid" else [r for r in RECIPES if not is_premium(r)]
    counts = {}
    for r in pool:
        cat = r.get("category") or "Other"
        counts[cat] = counts.get(cat, 0) + 1
    return sorted(
        [{"name": k, "count": v} for k, v in counts.items()],
        key=lambda x: -x["count"],
    )


@app.get("/api/recipe/{recipe_id}")
def get_recipe(recipe_id: int):
    for r in RECIPES:
        if r["id"] == recipe_id:
            return r
    raise HTTPException(404, "Recipe not found")


app.mount("/static", StaticFiles(directory=STATIC), name="static")'''

s = s.replace(needle, inject)

p.write_text(s)
print("main.py patched for category + recipe-by-id")
