# ==============================================================================
# IMPORTS
# ==============================================================================
import json
import os
from datetime import date, timedelta
from abc import ABC, abstractmethod


# ==============================================================================
# CONSTANT
# ==============================================================================
FILE: str = "data.json"

LEVEL_THRESHOLDS: tuple = (0, 100, 250, 500, 1000, 2000, 5000)
XP_BY_DIFFICULTY: dict = {
    "easy":   10,
    "medium": 20,
    "hard":   35,
}
MAX_LEVEL: int = len(LEVEL_THRESHOLDS) - 1


# ==============================================================================
# STORAGE
# ==============================================================================
def read_data() -> dict:
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_data(data: dict) -> None:
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ==============================================================================
# SPECIALISTE POO (Questions)
# ==============================================================================
class Question(ABC):
    def __init__(self, id: int, statement: str, subject: str, difficulty: int = 1, author: str = None, explanation: str = None) -> None:
        self.id = id
        self.statement = statement
        self.subject = subject
        self.difficulty = difficulty
        self.author = author
        self.explanation = explanation
        self.history: list = []

    @abstractmethod
    def verify_answer(self, answer: str) -> bool:
        pass

    @abstractmethod
    def display(self, highlight=None) -> str:
        pass

    def add_result(self, correct: bool) -> None:
        self.history.append(correct)

    @staticmethod
    def text_style(text: str, red: bool = False, underline: bool = False) -> str:
        codes = []
        if red: codes.append("31")
        if underline: codes.append("4")
        if not codes: return text
        return f"\033[{';'.join(codes)}m{text}\033[0m"

    def display_header(self) -> str:
        header = f"{self.subject} — Difficulty {self.difficulty}"
        if self.author:
            header += f" — Author: {self.author}"
        return header

    def display_explanation(self) -> str:
        return f"\nExplanation: {self.explanation}" if self.explanation else ""

    def score(self) -> str:
        if not self.history:
            return "No results"
        correct = sum(self.history)
        total = len(self.history)
        return f"{correct}/{total} ({correct * 100 / total:.0f}%)"

    def __str__(self) -> str:
        return f"[{self.id}] {self.statement} ({self.subject})"


class MultipleChoiceQuestion(Question):
    def __init__(self, id: int, statement: str, subject: str, choices: list, correct_answer: int, difficulty: int = 1, author: str = None, explanation: str = None) -> None:
        super().__init__(id, statement, subject, difficulty, author=author, explanation=explanation)
        self.choices = choices
        self.correct_answer = correct_answer

    def display(self, highlight: int = None) -> str:
        text = f"\n{self.display_header()}\n{self.statement}\n"
        for i, choice in enumerate(self.choices):
            index = f"{i}."
            if highlight is not None and highlight == i:
                index = self.text_style(index, red=True, underline=True)
            text += f"  {index} {choice}\n"
        return text

    def verify_answer(self, answer: str) -> bool:
        try:
            value = int(answer)
            is_correct = value == self.correct_answer
        except (ValueError, TypeError):
            is_correct = (str(answer).strip().lower() == str(self.choices[self.correct_answer]).strip().lower())
        self.add_result(is_correct)
        return is_correct


class TrueFalseQuestion(Question):
    def __init__(self, id: int, statement: str, subject: str, answer: bool, difficulty: int = 1, author: str = None, explanation: str = None) -> None:
        super().__init__(id, statement, subject, difficulty, author=author, explanation=explanation)
        self.answer = bool(answer)

    def display(self, highlight: str = None) -> str:
        text = f"\n{self.display_header()}\n{self.statement}\nTrue or False?"
        if highlight == "true":
            text = self.text_style(text, red=True, underline=True)
        return text

    def verify_answer(self, answer: str) -> bool:
        response = str(answer).strip().lower()
        if response in ["true", "t", "1", "yes", "y"]:
            choice = True
        elif response in ["false", "f", "0", "no", "n"]:
            choice = False
        else:
            choice = None
        is_correct = choice is not None and choice == self.answer
        self.add_result(is_correct)
        return is_correct


# ==============================================================================
# USERS
# ==============================================================================
class User:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.__xp: int = 0
        self.__level: int = 1
        self.__streak_days: int = 0
        self.__last_login: date = date.today()
        self.__score_history: dict = {}

    def get_xp(self) -> int: return self.__xp
    def get_level(self) -> int: return self.__level
    def get_streak(self) -> int: return self.__streak_days
    def get_history(self) -> dict: return self.__score_history

    def add_xp(self, points: int) -> None:
        if points < 0: return
        self.__xp += points
        print(f"+{points} XP earned! Total: {self.__xp} XP")
        self.__check_level()

    def update_streak(self) -> None:
        today: date = date.today()
        yesterday: date = today - timedelta(days=1)
        if self.__last_login == yesterday:
            self.__streak_days += 1
            print(f"Streak maintained: {self.__streak_days} consecutive day(s)!")
        elif self.__last_login < yesterday:
            self.__streak_days = 1
            print("Streak reset. New start: 1 day.")
        self.__last_login = today

    def record_score(self, subject: str, score: int) -> None:
        if subject not in self.__score_history:
            self.__score_history[subject] = []
        self.__score_history[subject].append(score)
        print(f"Score recorded: {score}/100 in {subject}.")

    def display_dashboard(self) -> None:
        print("\n" + "=" * 45)
        print(f"   DASHBOARD - {self.name.upper()}")
        print("=" * 45)
        print(f"   Level      : {self.__level}")
        print(f"   Total XP   : {self.__xp} XP")
        print(f"   Streak     : {self.__streak_days} day(s)")
        print("-" * 45)
        if not self.__score_history:
            print("   No quiz sessions recorded yet.")
        else:
            print("   Performance by subject:")
            for subject, scores in self.__score_history.items():
                average: float = sum(scores) / len(scores)
                print(f"   - {subject:<20} Avg: {average:.1f}/100 ({len(scores)} session(s))")
        print("=" * 45 + "\n")

    def identify_weak_points(self) -> list:
        weak_points: list = []
        for subject, scores in self.__score_history.items():
            average: float = sum(scores) / len(scores)
            if average < 50:
                weak_points.append((subject, round(average, 1)))
        return weak_points

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "xp": self.__xp,
            "level": self.__level,
            "streak_days": self.__streak_days,
            "last_login": str(self.__last_login),
            "score_history": self.__score_history,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(data["name"])
        user._User__xp = data.get("xp", 0)
        user._User__level = data.get("level", 1)
        user._User__streak_days = data.get("streak_days", 0)
        user._User__score_history = data.get("score_history", {})
        last_login = data.get("last_login", str(date.today()))
        user._User__last_login = date.fromisoformat(last_login)
        return user

    def __check_level(self) -> None:
        new_level: int = 1
        for i, threshold in enumerate(LEVEL_THRESHOLDS):
            if self.__xp >= threshold:
                new_level = i + 1
            else: break
        new_level = min(new_level, MAX_LEVEL)
        if new_level > self.__level:
            self.__level = new_level
            print(f"LEVEL UP! You are now level {self.__level}!")

    def __str__(self) -> str:
        return f"User(name={self.name}, level={self.__level}, xp={self.__xp})"


class PremiumUser(User):
    XP_MULTIPLIER: float = 1.5
    def __init__(self, name: str, subscription: str) -> None:
        super().__init__(name)
        self.subscription: str = subscription

    def add_xp(self, points: int) -> None:
        bonus_points: int = int(points * self.XP_MULTIPLIER)
        print(f"[Premium] XP bonus applied: {points} -> {bonus_points} XP")
        super().add_xp(bonus_points)

    def __str__(self) -> str:
        return f"PremiumUser(name={self.name}, subscription={self.subscription})"


# ==============================================================================
# UTILS
# ==============================================================================
def sort_questions_by_spacing(questions_list: list) -> list:
    return sorted(questions_list, key=lambda q: q.get("incorrect_attempts", 0), reverse=True)

def display_analytics_dashboard(user_object) -> None:
    print("\n" + "=" * 45)
    print(f"   ACADEMIC ANALYTICS - {user_object.name.upper()}")
    print("=" * 45)
    history: dict = user_object.get_history()
    if not history:
        print("   No performance data available yet.")
        print("=" * 45 + "\n")
        return
    print("   Calculated averages by subject:\n")
    for subject, scores in history.items():
        if len(scores) == 0: continue
        average: float = sum(scores) / len(scores)
        print(f"   - {subject:<20} : {average:.1f}/100")
        if average < 50:
            print(" Low performance detected. Review recommended.")
    print("=" * 45 + "\n")


# ==============================================================================
# ENGIN
# ==============================================================================
class SessionQuiz:
    def __init__(self, questions: list, user) -> None:
        self.questions = questions
        self.user = user
        self.score: int = 0
        self.total: int = len(questions)
        self.resultats: list = []

    def display_entete(self) -> None:
        print("=" * 50)
        print(f"  Welcome, {self.user.name}!")
        print(f"  Level: {self.user.get_level()} | XP: {self.user.get_xp()}")
        print(f"  Number of questions: {self.total}")
        print("=" * 50)
        print()

    def ask_question(self, question: Question, number: int) -> bool:
        print(f"  Question {number}/{self.total}: {question.statement}")
        print(f"  Difficulty: {question.difficulty}")
        if hasattr(question, "choices"):
            for i, choice in enumerate(question.choices, start=1):
                print(f"    {i}. {choice}")
        try:
            answer = input("\n  Your answer: ").strip()
        except (EOFError, KeyboardInterrupt):
            answer = ""
        correct = question.verify_answer(answer)
        if correct: print("  Good answer! +XP")
        else: print("   Wrong.")
        print()
        return correct

    def throw(self) -> None:
        self.display_entete()
        number: int = 1
        while number <= self.total:
            question = self.questions[number - 1]
            correct = self.ask_question(question, number)
            if correct:
                self.score += 1
                self.user.add_xp(10 * question.difficulty)
            self.resultats.append({"question": question.statement, "correct": correct})
            number += 1
        self.display_result()

    def display_result(self) -> None:
        percentage: float = (self.score / self.total * 100) if self.total > 0 else 0
        print("=" * 50)
        print("             END OF SESSION")
        print("=" * 50)
        print(f"  Player  : {self.user.name}")
        print(f"  Score   : {self.score}/{self.total} ({percentage:.1f}%)")
        print(f"  XP      : {self.user.get_xp()}")
        print(f"  Level   : {self.user.get_level()}")
        print("=" * 50)
        self.user.update_streak()
        print(f"  Streak  : {self.user.get_streak()} day(s)\n")


# ==============================================================================
# MAIN 
# ==============================================================================
def display_welcome(name: str, total: int) -> None:
    print("\n" + "=" * 50)
    print(f"  Welcome to Educ X, {name}!")
    print(f"  You have {total} question(s) today. Good luck!")
    print("=" * 50 + "\n")

def display_final_score(score: int, total: int) -> None:
    percentage: float = (score / total * 100) if total > 0 else 0
    print("=" * 50)
    print(f"  Final score: {score}/{total} ({percentage:.1f}%)")
    if percentage == 100: print("  Perfect score! Outstanding work! ")
    elif percentage >= 70: print("  Great job! Keep it up ")
    elif percentage >= 40: print("  Not bad, but there is room to improve.")
    else: print("  Tough session. Review the material and try again")
    print("=" * 50 + "\n")

def run_quiz() -> None:
    data: dict = read_data()
    questions: list = data.get("questions", [])
    user: dict = data.get("user", {})

    if not user.get("name"):
        user["name"] = input("  What is your name? ").strip()

    user.setdefault("score", 0)
    user.setdefault("history", [])

    if not questions:
        print("  No questions found in data.json. Please add some first.")
        return

    display_welcome(user["name"], len(questions))

    score: int = 0
    question_number: int = 1

    for q in questions:
        print(f"  [{question_number}/{len(questions)}] {q['question']}")
        answer: str = input("  Your answer: ").strip()

        if answer.lower() == q.get("answer", "").lower():
            print(" Correct!\n")
            score += 1
        else:
            print(f"Wrong. The answer was: {q.get('answer', '')}\n")

        question_number += 1

    display_final_score(score, len(questions))

    user["score"] = score
    user["history"].append(score)
    data["user"] = user

    write_data(data)
    print("  Progress saved. See you next time!\n")

if __name__ == "__main__":
    run_quiz()