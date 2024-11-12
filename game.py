from typing import List

'''
Game class
Used to represent a game
'''
class Game:
    def __init__(self, name: str, release_date: str, studio: str, ratings: int, platforms: List[str]):
        self.name = name
        self.release_date = release_date
        self.studio = studio
        self.ratings = ratings
        self.platforms = platforms

    def to_dict(self):
        return {
            "name": self.name,
            "release_date": self.release_date,
            "studio": self.studio,
            "ratings": self.ratings,
            "platforms": self.platforms
        }
