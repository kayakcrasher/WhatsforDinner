"""API tests for What's for Dinner."""


def test_index_serves_html(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "What's for Dinner" in r.text


def test_list_recipes_returns_data(client):
    r = client.get("/api/recipes")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] > 0
    assert data["total"] >= data["count"]
    assert isinstance(data["recipes"], list)
    assert "name" in data["recipes"][0]


def test_spin_returns_a_recipe(client):
    r = client.get("/api/spin")
    assert r.status_code == 200
    recipe = r.json()
    assert "name" in recipe
    assert "ingredients" in recipe
    assert "steps" in recipe


def test_categories_endpoint(client):
    r = client.get("/api/categories")
    assert r.status_code == 200
    cats = r.json()
    assert isinstance(cats, list)
    assert all("name" in c and "count" in c for c in cats)


def test_recipe_by_id(client):
    all_r = client.get("/api/recipes").json()["recipes"]
    first_id = all_r[0]["id"]
    r = client.get(f"/api/recipe/{first_id}")
    assert r.status_code == 200
    assert r.json()["id"] == first_id


def test_recipe_by_id_404(client):
    r = client.get("/api/recipe/999999")
    assert r.status_code == 404


def test_vegetarian_filter_excludes_meat(client):
    r = client.get("/api/recipes?vegetarian=true&tier=paid")
    recipes = r.json()["recipes"]
    assert len(recipes) > 0
    for recipe in recipes:
        blob = " ".join(recipe["ingredients"]).lower()
        for meat in ["chicken", "beef", "pork", "lamb", "shrimp", "bacon"]:
            assert meat not in blob, f"{recipe['name']} has {meat}"


def test_no_peanuts_filter(client):
    r = client.get("/api/recipes?no_peanuts=true&tier=paid")
    recipes = r.json()["recipes"]
    for recipe in recipes:
        blob = " ".join(recipe["ingredients"]).lower()
        assert "peanut" not in blob


def test_free_tier_hides_premium(client):
    free = client.get("/api/recipes?tier=free").json()["recipes"]
    paid = client.get("/api/recipes?tier=paid").json()["recipes"]
    assert len(free) < len(paid)
    assert all(not r.get("premium") for r in free)


def test_paid_tier_includes_premium(client):
    recipes = client.get("/api/recipes?tier=paid").json()["recipes"]
    assert any(r.get("premium") for r in recipes)


def test_meal_type_filter(client):
    r = client.get("/api/recipes?meal_type=dessert&tier=paid")
    recipes = r.json()["recipes"]
    assert len(recipes) > 0
    for recipe in recipes:
        assert recipe.get("meal_type") == "dessert"


def test_protein_filter(client):
    r = client.get("/api/recipes?protein=chicken&tier=paid")
    recipes = r.json()["recipes"]
    assert len(recipes) > 0
    for recipe in recipes:
        assert recipe.get("protein") == "chicken"


def test_combined_filters(client):
    r = client.get("/api/recipes?vegetarian=true&meal_type=dinner&tier=paid")
    recipes = r.json()["recipes"]
    for recipe in recipes:
        assert recipe.get("meal_type") == "dinner"
        assert recipe.get("protein") == "vegetarian"


def test_spin_respects_filters(client):
    for _ in range(20):
        r = client.get("/api/spin?meal_type=dessert&tier=paid")
        assert r.status_code == 200
        recipe = r.json()
        assert recipe.get("meal_type") == "dessert"
