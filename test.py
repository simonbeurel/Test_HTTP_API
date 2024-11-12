import requests

# URL de base du serveur Flask
BASE_URL = "http://127.0.0.1:5000"

def test_clear_games():
    print("[+] Trying to delete all of the games... [+]")
    response = requests.delete(f"{BASE_URL}/clear_games")
    print(response.json())
    assert response.status_code == 200

def test_add_game():
    print("[+] Adding a new game (The Witcher 3: Wild Hunt) [+]")
    game_data = {
        "name": "The Witcher 3: Wild Hunt",
        "release_date": "2015-05-19",
        "studio": "CD Projekt Red",
        "ratings": 19,
        "platforms": ["PC", "PS4", "PS5", "Switch", "One"]
    }
    response = requests.post(f"{BASE_URL}/add_game", json=game_data)
    print(response.json())
    assert response.status_code == 201

def test_get_games():
    print("[+] Retrieving all games [+]")
    response = requests.get(f"{BASE_URL}/games")
    print(response.json())
    assert response.status_code == 200

def test_get_game_by_name():
    print("[+] Retrieving The Witcher 3: Wild Hunt [+]")
    game_name = "The Witcher 3: Wild Hunt"
    response = requests.get(f"{BASE_URL}/game/{game_name}")
    print(response.json())
    assert response.status_code == 200

def test_update_game():
    print("[+] Updating The Witcher 3: Wild Hunt with a different rating[+]")
    game_data = {
        "name": "The Witcher 3: Wild Hunt",
        "release_date": "2015-05-19",
        "studio": "CD Projekt Red",
        "ratings": 500,
        "platforms": ["PC", "PS4", "PS5", "Switch", "One"]
    }
    response = requests.put(f"{BASE_URL}/update_game", json=game_data)
    print(response.json())
    assert response.status_code == 200

def test_best_game_of_the_current_year():
    game_data = {
        "name": "Les Simpsons",
        "release_date": "2024-05-19",
        "studio": "Garfield",
        "ratings": 502,
        "platforms": ["PC", "PS4", "PS5", "Switch", "One"]
    }
    response = requests.post(f"{BASE_URL}/add_game", json=game_data)
    print("[+] Retrieving the best game of the current year[+]")
    response = requests.get(f"{BASE_URL}/best_game_of_the_current_year")
    print(response.json())
    assert response.status_code == 200

def test_delete_game():
    print("[+] Deleting The Witcher 3: Wild Hunt[+]")
    game_name = {"name": "The Witcher 3: Wild Hunt"}
    response = requests.delete(f"{BASE_URL}/delete_game", json=game_name)
    print(response.json())
    assert response.status_code == 200 or response.status_code == 404

def test_login(username, password):
    print("[+] Trying to login...[+]")
    login_data = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(response.json())
    assert response.status_code == 200 or response.status_code == 401


def test_to_similar_names():
    print("[+] Test adding 2 games GameAAAA & GameAAAB [+]")
    print("[+] Adding a new game (GameAAAA) [+]")
    game_data = {
        "name": "GameAAAA",
        "release_date": "2024",
        "studio": "Ubisoft",
        "ratings": 19,
        "platforms": ["PC"]
    }
    response = requests.post(f"{BASE_URL}/add_game", json=game_data)
    assert response.status_code == 201

    print("[+] Adding a new game (GameAAAB) [+]")
    game_data = {
        "name": "GameAAAB",
        "release_date": "2024",
        "studio": "Ubisoft",
        "ratings": 19,
        "platforms": ["PC"]
    }
    response = requests.post(f"{BASE_URL}/add_game", json=game_data)
    print(response.json())
    assert response.status_code == 400


if __name__ == "__main__":
    test_clear_games()
    test_add_game()
    test_get_games()
    test_get_game_by_name()
    test_update_game()
    test_best_game_of_the_current_year()
    test_delete_game()
    test_login("admin", "simon")
    test_to_similar_names()
