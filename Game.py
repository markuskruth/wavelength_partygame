import random, copy, math
class Game:
    def __init__(self, player_count, player_names, rounds=5):
        self.player_count = player_count
        self.player_names = player_names
        self.hint_giver_index = 0
        self.rounds = rounds
        self.target_angle = random.randint(0, 180) * math.pi / 180  # Random target angle in radians
        self.player_scores = {name: 0 for name in player_names}
        self.questions = [
                        ("Aliarvostettu elokuva", "Yliarvostettu elokuva"),
                        ("Pahan makuinen ruoka", "Hyvän makuinen ruoka"),
                        ("Testi vasen", "Testi oikea")
                        ]
        random.shuffle(self.questions)
        self.question_index = 0
        self.hint_giver = player_names[0]

        # List of players whose turn it can be
        self.possible_turns = copy.deepcopy(self.player_names)
        self.possible_turns.remove(self.hint_giver)
        random.shuffle(self.possible_turns)

        self.turn_index = 0
        self.turn = self.possible_turns[self.turn_index]
        self.guesses = {name: 0 for name in self.possible_turns}
        self.new_round = False

    
    def next_turn(self):
        self.turn_index += 1
        if self.turn_index >= len(self.possible_turns):
            return False
        else:
            self.turn = self.possible_turns[self.turn_index]
            return True
    
    def end_round(self, target_angle, guesses):
        target_angle_degrees = target_angle * 180/math.pi
        for player in self.possible_turns:
            guess = guesses[player]
            difference = guess - target_angle_degrees
            if difference >= 0:
                if difference <= 10:
                    self.player_scores[player] += 3
                elif difference <= 20:
                    self.player_scores[player] += 2
                elif difference <= 30:
                    self.player_scores[player] += 1
            else:
                if abs(difference) <= 10:
                    self.player_scores[player] += 2
                elif abs(difference) <= 20:
                    self.player_scores[player] += 1

    def start_round(self):
        self.hint_giver_index += 1
        self.hint_giver = self.player_names[self.hint_giver_index % len(self.player_names)]

        self.possible_turns = copy.deepcopy(self.player_names)
        self.possible_turns.remove(self.hint_giver)
        random.shuffle(self.possible_turns)
        self.turn_index = 0
        self.turn = self.possible_turns[self.turn_index]
        self.guesses = {name: 0 for name in self.possible_turns}
        self.new_round = True
    
    def next_question(self):
        question = self.questions[self.question_index]
        self.question_index += 1
        return question

    def next_target_angle(self):
        self.target_angle = random.randint(0, 180) * math.pi / 180
        return self.target_angle
