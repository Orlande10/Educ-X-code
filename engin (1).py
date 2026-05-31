"""
engin.py
Defines the SessionQuiz class which manages a full interactive quiz session.
Receives a list of Question objects and a User, runs through each question,
tracks the score, awards XP, and displays a summary at the end.
"""

from specialiste_poo import Question


class SessionQuiz:
    """
    Manages a complete quiz session in the terminal.
    Iterates through a list of Question objects, asks each one,
    records the result, awards XP for correct answers, and
    prints a final score summary when all questions are done.
    """

    def __init__(self, questions: list, user) -> None:
        """
        Initialises the session with the selected questions and the playing user.

        Args:
            questions (list): A list of Question objects (MCQ, TrueFalse, etc.).
            user (User): The User instance currently playing.
        """
        self.questions = questions
        self.user = user
        self.score: int = 0
        self.total: int = len(questions)
        self.resultats: list = []  # stores per-question outcome dicts

    def display_entete(self) -> None:
        """
        Prints a welcome header at the start of the session,
        showing the player's name, level, XP, and number of questions.
        """
        print("=" * 50)
        print(f"  Welcome, {self.user.name}!")
        print(f"  Level: {self.user.get_level()} | XP: {self.user.get_xp()}")
        print(f"  Number of questions: {self.total}")
        print("=" * 50)
        print()

    def ask_question(self, question: Question, number: int) -> bool:
        """
        Displays a single question, collects the user's answer,
        and returns whether the answer was correct.

        Args:
            question (Question): The question object to ask.
            number (int): The position of this question in the session (1-based).

        Returns:
            bool: True if the answer was correct, False otherwise.
        """
        print(f"  Question {number}/{self.total}: {question.statement}")
        print(f"  Difficulty: {question.difficulty}")

        # If the question has multiple choices, display them
        if hasattr(question, "choices"):
            for i, choice in enumerate(question.choices, start=1):
                print(f"    {i}. {choice}")

        try:
            answer = input("\n  Your answer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Input interrupted.")
            answer = ""

        correct = question.verify_answer(answer)

        if correct:
            print(" Good answer! +XP")
        else:
            print(f" Wrong. The correct answer was: {question.choices[question.correct_answer] if hasattr(question, 'choices') else '—'}")
        print()

        return correct

    def throw(self) -> None:
        """
        Main loop of the quiz session.
        Goes through every question using a while loop,
        updates the score, awards XP, and records each result.
        """
        self.display_entete()

        number: int = 1
        while number <= self.total:
            question = self.questions[number - 1]
            correct = self.ask_question(question, number)

            if correct:
                self.score += 1
                xp_win = 10 * question.difficulty  # more XP for harder questions
                self.user.add_xp(xp_win)

            # Record the outcome of this question
            self.resultats.append({
                "question": question.statement,
                "correct": correct
            })

            number += 1

        self.display_result()

    def display_result(self) -> None:
        """
        Prints the end-of-session summary: score, success rate,
        total XP, current level, and updated streak.
        """
        percentage: float = (self.score / self.total * 100) if self.total > 0 else 0

        print("=" * 50)
        print("             END OF SESSION")
        print("=" * 50)
        print(f"  Player: {self.user.name}")
        print(f"  Score : {self.score}/{self.total} ({percentage:.1f}%)")
        print(f"  XP: {self.user.get_xp()}")
        print(f"  Level: {self.user.get_level()}")
        print("=" * 50)

        self.user.update_streak()
        print(f"Streak : {self.user.get_streak()} day(s)")
        print()
