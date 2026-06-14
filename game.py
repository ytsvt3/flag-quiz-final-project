import json
import os
import random
from data import BY_DIFFICULTY, ROUNDS, TIMER_SECONDS, BASE_POINTS, SPEED_BONUS_MAX

SCORES_FILE = os.path.join(os.path.dirname(__file__), "scores.json")


class Game:
    def __init__(self):
        self.player_name = ""
        self.difficulty = "easy"
        self.score = 0
        self.round_num = 0
        self.questions = []
        self.current_question = None
        self.last_result = None
        self.leaderboard = self._load_leaderboard()

    def start(self, player_name: str, difficulty: str):
        self.player_name = player_name
        self.difficulty = difficulty
        self.score = 0
        self.round_num = 0
        pool = list(BY_DIFFICULTY[difficulty])
        random.shuffle(pool)
        self.questions = pool[:ROUNDS]
        self.last_result = None

    def next_question(self) -> bool:
        if self.round_num >= len(self.questions):
            return False
        entry = self.questions[self.round_num]
        self.round_num += 1
        wrong_pool = [f for f in BY_DIFFICULTY[self.difficulty] if f["name"] != entry["name"]]
        wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))
        options = [entry["name"]] + [w["name"] for w in wrongs]
        random.shuffle(options)
        self.current_question = {
            "flag": entry,
            "options": options,
            "correct": entry["name"],
        }
        return True

    def answer(self, chosen: str, time_left: float) -> dict:
        correct = self.current_question["correct"]
        is_correct = chosen == correct
        points = 0
        if is_correct:
            speed_bonus = int(SPEED_BONUS_MAX * (time_left / TIMER_SECONDS))
            points = BASE_POINTS + speed_bonus
            self.score += points
        self.last_result = {
            "correct": is_correct,
            "chosen": chosen,
            "answer": correct,
            "points_earned": points,
            "total_score": self.score,
            "round": self.round_num,
            "total_rounds": ROUNDS,
        }
        return self.last_result

    def timeout(self) -> dict:
        return self.answer("", 0)

    def save_score(self):
        self.leaderboard.append({"name": self.player_name, "score": self.score})
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        self.leaderboard = self.leaderboard[:10]
        try:
            with open(SCORES_FILE, "w") as f:
                json.dump(self.leaderboard, f)
        except Exception:
            pass

    def _load_leaderboard(self) -> list:
        try:
            with open(SCORES_FILE) as f:
                return json.load(f)
        except Exception:
            return []

    @property
    def is_done(self) -> bool:
        return self.round_num >= ROUNDS
