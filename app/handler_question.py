import json
import re
import nltk
from typing import Dict

nltk.download('punkt_tab')

class AnswerToQuestion:
    def __init__(self, path = 'app/static/question.json', best_rank: int = 70, column='video_snapshots'):
        self.dataOfQuestion = self.load_data(path)[column]
        self.best_rank = best_rank
        self.failure_phrases = "Пожалуйста, перефразируйте вопрос"

    def __call__(self, text):
        intention = self.get_intent(text)
        if intention:
            return intention
        return self.failure_phrases

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower()
        punctuation = r"[^\w\s]"
        return re.sub(punctuation, '', text)

    @staticmethod
    def load_data(path: str) -> Dict[str, Dict[str, list]]:
        with open(path, encoding='utf-8') as file:
            return json.load(file)

    def get_rank_normalize(self, text_1: str, text_2: str):
        texts = tuple(map(self.normalize, (text_1, text_2)))
        distance = nltk.edit_distance(*texts)
        average_length = sum(map(len, texts)) / 2
        return distance / average_length * 100

    def get_intent(self, text):
        best_rank = self.best_rank
        result = None
        for name, data in self.dataOfQuestion.items():
            for question in data['question']:
                rank = self.get_rank_normalize(text, question)
                if rank < best_rank:
                    best_rank = rank
                    result = name
        return result

text = input('Question: ')
answer = AnswerToQuestion()
intention = answer(text)
print('Answer:', intention)