from abc import ABC, abstractmethod

class Question(ABC):
    def __init__(self, id, statement, subject, difficulty=1, author=None, explanation=None):
        self.id = id
        self.statement = statement
        self.subject = subject
        self.difficulty = difficulty
        self.author = author
        self.explanation = explanation
        self.history = []  # [True, False, True] to track answers

    @abstractmethod
    def verify_answer(self, answer):
        pass

    @abstractmethod
    def display(self):
        pass

    def add_result(self, correct):
        self.history.append(correct)

    @staticmethod
    def text_style(text, red=False, underline=False):
        codes = []
        if red:
            codes.append("31")
        if underline:
            codes.append("4")
        if not codes:
            return text
        return f"\033[{';'.join(codes)}m{text}\033[0m"

    def display_header(self):
        header = f"{self.subject} — Difficulty {self.difficulty}"
        if self.author:
            header += f" — Author: {self.author}"
        return header

    def display_explanation(self):
        return f"\nExplanation: {self.explanation}" if self.explanation else ""

    def score(self):
        if not self.history:
            return "No results"
        correct = sum(self.history)
        total = len(self.history)
        return f"{correct}/{total} ({correct * 100 / total:.0f}%)"

    def __str__(self):
        return f"[{self.id}] {self.statement} ({self.subject})"

class MultipleChoiceQuestion(Question):
    def __init__(self, id, statement, subject, choices, correct_answer, difficulty=1, author=None, explanation=None):
        super().__init__(id, statement, subject, difficulty, author=author, explanation=explanation)
        self.choices = choices  # ["Paris", "Lyon", "Marseille"]
        self.correct_answer = correct_answer  # index 0, 1, 2...

    def display(self, highlight=None):
        text = f"\n{self.display_header()}\n{self.statement}\n"
        for i, choice in enumerate(self.choices):
            index = f"{i}."
            if highlight is not None and highlight == i:
                index = self.text_style(index, red=True, underline=True)
            line = f"  {index} {choice}"
            text += f"{line}\n"
        return text

    def verify_answer(self, answer):
        try:
            value = int(answer)
            is_correct = value == self.correct_answer
        except (ValueError, TypeError):
            is_correct = str(answer).strip().lower() == str(self.choices[self.correct_answer]).strip().lower()
        self.add_result(is_correct)
        return is_correct

class TrueFalseQuestion(Question):
    def __init__(self, id, statement, subject, answer, difficulty=1, author=None, explanation=None):
        super().__init__(id, statement, subject, difficulty, author=author, explanation=explanation)
        self.answer = bool(answer)

    def display(self, highlight=None):
        text = f"\n{self.display_header()}\n{self.statement}\nTrue or False?"
        if highlight == 'true':
            text = self.text_style(text, red=True, underline=True)
        return text

    def verify_answer(self, answer):
        response = str(answer).strip().lower()
        true = response in ["true", "t", "1", "yes", "y", "oui", "o"]
        false = response in ["false", "f", "0", "no", "n", "non"]
        if true:
            choice = True
        elif false:
            choice = False
        else:
            choice = None
        is_correct = choice is not None and choice == self.answer
        self.add_result(is_correct)
        return is_correct
