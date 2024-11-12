from flask import Flask, request, jsonify
from pymongo import MongoClient
from game import Game
import random
import hashlib
from fuzzywuzzy import fuzz
app = Flask(__name__)

client = MongoClient("mongodb://root:examplepassword@mongodb:27017/")
db = client["mydatabase"]
collection = db["games_hanfang"]

collection_users = db["users_hanfang"]
# We add an admin user to the database (password hash with SHA-256)
collection_users.insert_one({"username": "admin", "password": "0a5d17d3b19f82f8340d3977609aa9e86b4ad8b9bd71bd9eced9271f1d5b2e4a"})

'''
login function: Used to authenticate a user
Return 200 if the user is authenticated and a connection key (needed for every actions)
'''
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username or password required"}), 400
    # Hash the password with SHA-256
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    # Check if the user exists in the database
    user = collection_users.find_one({"username": username, "password": password_hash})
    if user:
        connection_key = random.randint(1,50)
        collection_users.update_one({"username": username}, {"$set": {"connection_timeout": 3600, "connection_key":connection_key}})
        return jsonify({"message": "Successful connection","connection_key": connection_key}), 200
    else:
        return jsonify({"error": "Username or password incorrect"}), 401

'''
clea_games function: Used to delete all games in the database
Return 200 if all games are deleted
'''
@app.route('/clear_games', methods=['DELETE'])
def clear_games():
    # Delete all games in the database
    collection.delete_many({})
    return jsonify({"message": "All games are now deleted."}), 200

'''
add_game function: Used to add a game in the database
Return 201 if the game is added or 400 if at least one data is missing
'''
@app.route('/add_game', methods=['POST'])
def add_game():
    data = request.get_json()
    try:
        game_name = data['name']

        # Check if the game name is too similar to an existing one
        all_games = list(collection.find({}, {"_id": 0, "name": 1}))
        for existing_game in all_games:
            similarity = fuzz.ratio(game_name.lower(), existing_game['name'].lower())
            if similarity > 80:
                return jsonify({"error": f"The name is too similar with the game '{existing_game['name']}'."}), 400
        # Create a Game object
        game = Game(
            name=data['name'],
            release_date=data['release_date'],
            studio=data['studio'],
            ratings=data['ratings'],
            platforms=data['platforms']
        )
        # Insert the game in the database
        collection.insert_one(game.to_dict())
        return jsonify({"message": "The game was added with success"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing data : {e}"}), 400


'''
delete_game function: Used to delete a game in the database
Return 200 if the game is deleted or 404 if the game is not found
'''
@app.route('/delete_game', methods=['DELETE'])
def delete_game():
    data = request.get_json()  # Récupérer les données JSON de la requête
    game_name = data.get('name')
    if not game_name:
        return jsonify({"error": "The game's name is required for the deletion"}), 400
    # Delete the game in the database
    result = collection.delete_one({"name": game_name})
    if result.deleted_count > 0:
        return jsonify({"message": f"The game '{game_name}' was deleted."}), 200
    else:
        return jsonify({"error": f"None game was find with the name '{game_name}'"}), 404

'''
get_games function: Used to get all games in the database
Return the list of games in the database
'''
@app.route('/games', methods=['GET'])
def get_games():
    # Get all games in the database
    games = list(collection.find({}, {"_id": 0}))
    return jsonify(games)

'''
get_game_by_name function: Used to get a game by its name
Return the game if it exists or 404 if the game is not found
'''
@app.route('/game/<name>', methods=['GET'])
def get_game_by_name(name):
    # Get a game by its name
    game = collection.find_one({"name": name}, {"_id": 0})
    if game:
        return jsonify(game)
    else:
        return jsonify({"error": f"None game was find with the name '{name}'"}), 404

'''
update_game function: Used to update a game in the database
Return 200 if the game is updated or 400 if there is not name in the data sended and 404 if the game is not found
'''
@app.route('/update_game', methods=['PUT'])
def update_game():
    data = request.get_json()
    game_name = data.get('name')
    if not game_name:
        return jsonify({"error": "The game's name is required for an update"}), 400
    # Update the game in the database
    game = collection.find_one({"name": game_name})
    if not game:
        return jsonify({"error": f"None game was find with the name '{game_name}'"}), 404
    # Update the game with the new data
    update_data = {}
    if 'release_date' in data:
        update_data['release_date'] = data['release_date']
    if 'studio' in data:
        update_data['studio'] = data['studio']
    if 'ratings' in data:
        update_data['ratings'] = data['ratings']
    if 'platforms' in data:
        update_data['platforms'] = data['platforms']
    # Update the game in the database
    collection.update_one({"name": game_name}, {"$set": update_data})
    return jsonify({"message": f"The game '{game_name}' is updated successfully!"}), 200


@app.route('/best_game_of_the_current_year', methods=['GET'])
def best_game_of_the_current_year():
    # Get all games in the database
    games = list(collection.find({}, {"_id": 0}))
    # Get the best game of the current year
    best_game = max(games, key=lambda x: x['ratings'])
    return jsonify(best_game)

'''
Main function: Used to run the server on the port 5000
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
