from validators import validate_recipe


def test_validate_recipe():
    """
    test to validate recipe
    """
    recipe = {
        "name": "chicken",
        "category": "dinner",
        "user_name": "test4",
        "title": "chciken",
        "serves": "4",
        "mail": "test@test.com",
        "image_url": "www.test.com",
        "ingredients": ["chicken", "onion"],
        "instructions": ["cut", "slice"],
    }

    result = validate_recipe(recipe)
    assert result is True  # here we check if result is correct, recipe valid
    recipe["instructions"] = []
    result = validate_recipe(recipe)
    assert result is False  # here we check if result is corect, recipe invalid


if __name__ == "__main__":
    test_validate_recipe()