import math
from collections import defaultdict

TRAINING_CORPUS = [
    "password", "123456", "123456789", "guest", "qwerty", "12345678", "111111",
    "12345", "colombia", "123123", "admin", "welcome", "ninja", "football",
    "iloveyou", "master", "sunshine", "princess", "charlie", "dragon",
    "monkey", "letmein", "shadow", "superman", "trustno1", "computer"
]

class MarkovPasswordModel:
    def __init__(self, n=2):
        self.n = n
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.totals = defaultdict(int)
        self.train(TRAINING_CORPUS)

    def train(self, corpus):
        for word in corpus:
            padded = "^" + word.lower() + "$"
            for i in range(len(padded) - self.n):
                gram = padded[i:i + self.n]
                next_char = padded[i + self.n]
                self.transitions[gram][next_char] += 1
                self.totals[gram] += 1

    def calculate_perplexity(self, password: str) -> float:
        """Lower perplexity indicates higher predictability according to common leaks."""
        padded = "^" + password.lower() + "$"
        log_prob = 0.0
        count = 0
        vocab_size = 128  # Laplace smoothing base

        for i in range(len(padded) - self.n):
            gram = padded[i:i + self.n]
            next_char = padded[i + self.n]
            numerator = self.transitions[gram][next_char] + 1
            denominator = self.totals[gram] + vocab_size
            log_prob += math.log2(numerator / denominator)
            count += 1

        if count == 0:
            return 999.0
        cross_entropy = -log_prob / count
        return round(2 ** cross_entropy, 2)

    def predict_next_chars(self, prefix: str, top_k=3):
        gram = ("^" + prefix.lower())[-self.n:]
        predictions = sorted(self.transitions[gram].items(), key=lambda x: x[1], reverse=True)
        return [char for char, _ in predictions[:top_k] if char != "$"]

ml_model = MarkovPasswordModel()