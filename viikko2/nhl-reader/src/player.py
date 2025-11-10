import requests

class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict["nationality"]
        self.goals = dict["goals"]
        self.assists = dict["assists"]

    def __str__(self):
        return f"{self.name:20} {self.goals}+{self.assists}={self.goals+self.assists}"

class PlayerReader:
    def __init__(self, url):
        self.url = url

    def get_players(self):
        response = requests.get(self.url).json()
        players = []
        for player_dict in response:
            players.append(Player(player_dict))

        return players

class PlayerStats():
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        players_by_nationality = [p for p in self.players if p.nationality == nationality]
        players_by_nationality.sort(key=lambda p: p.goals+p.assists, reverse=True)

        return players_by_nationality
