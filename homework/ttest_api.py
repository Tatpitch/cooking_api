import requests

def get_one_recipe(recipe_id: int):
    url = f"http://127.0.0.1:8000/recipes/{recipe_id}"
    response = requests.get(url)
    return response.json()


if __name__ == '__main__':
    recipe = get_one_recipe(4)
    print(recipe)
