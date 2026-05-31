"""
main.py
Entry point for the Educ X quiz application.
Loads questions and user data from storage, runs the quiz loop,
displays the result, and saves progress back to the JSON file.
"""

from storage import read_data, write_data


def display_welcome(name: str, total: int) -> None:
    """
    Prints a welcome message at the start of the quiz.

    Args:
        name (str): The player's name.
        total (int): Total number of questions in this session.
    """
    print("\n" + "=" * 50)
    print(f"  Welcome to Educ X, {name}!")
    print(f"  You have {total} question(s) today. Good luck!")
    print("=" * 50 + "\n")


def display_final_score(score: int, total: int) -> None:
    """
    Prints the final score and a motivational message based on the result.

    Args:
        score (int): Number of correct answers.
        total (int): Total number of questions.
    """
    percentage: float = (score / total * 100) if total > 0 else 0

    print("=" * 50)
    print(f"  Final score: {score}/{total} ({percentage:.1f}%)")

    # Give different feedback depending on how well the user did
    if percentage == 100:
        print("Perfect score! Outstanding work! ")
    elif percentage >= 70:
        print("Great job! Keep it up! ")
    elif percentage >= 40:
        print("Not bad, but there is room to improve.")
    else:
        print("Tough session. Review the material and try again ")

    print("=" * 50 + "\n")


def run_quiz() -> None:
    """
    Main function that runs the Educ X quiz.
    Loads data from the JSON file, collects the player's name if needed,
    iterates through all questions using a for loop, tracks the score,
    and saves the updated user data back to storage when done.
    """
    data: dict = read_data()

    questions: list = data.get("questions", [])
    user: dict = data.get("user", {})

    # Ask for the player's name if this is their first time
    if not user.get("name"):
        user["name"] = input("  What is your name? ").strip()

    # Make sure all required keys exist before using them
    user.setdefault("score", 0)
    user.setdefault("history", [])

    if not questions:
        print("  No questions found in data.json. Please add some first.")
        return

    display_welcome(user["name"], len(questions))

    score: int = 0
    question_number: int = 1  # used alongside the for loop for display

    for q in questions:
        print(f"  [{question_number}/{len(questions)}] {q['question']}")
        answer: str = input("  Your answer: ").strip()

        if answer.lower() == q["answer"].lower():
            print("  ✔ Correct!\n")
            score += 1
        else:
            print(f"  ✖ Wrong. The answer was: {q['answer']}\n")

        question_number += 1

    display_final_score(score, len(questions))

    # Update and save the user's progress
    user["score"] = score
    user["history"].append(score)  # history is a list of past scores
    data["user"] = user

    write_data(data)
    print("  Progress saved. See you next time\n")


if __name__ == "__main__":
    run_quiz()
