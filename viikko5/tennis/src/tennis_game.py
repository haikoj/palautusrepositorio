class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.score_player1 = 0
        self.score_player2 = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.score_player1 += 1
        else: self.score_player2 += 1
        
    def get_score(self):
        self.scores = ["Love", "Fifteen", "Thirty", "Forty"]
        if self.score_player1 == self.score_player2:
            return self.even()
        if self.score_player1 >= 4 or self.score_player2 >= 4:
            return self.over40()
        return self.under40 ()
    
    def even(self):
        if self.score_player1 <= 2:
            return f"{self.scores[self.score_player1]}-All"
        return "Deuce"
    
    def under40(self):
        return f"{self.scores[self.score_player1]}-{self.scores[self.score_player2]}"
    
    def over40(self):
        diff = self.score_player1 - self.score_player2

        if diff >= 2:
            return f"Win for {self.player1_name}"
        if diff <= -2:
            return f"Win for {self.player2_name}"
        if diff == 1:
            return f"Advantage {self.player1_name}"
        return f"Advantage {self.player2_name}"