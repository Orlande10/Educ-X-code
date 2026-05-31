"""
utils.py
Utility functions for spaced repetition sorting and analytics display.
These functions operate on question lists and user objects without modifying them.
"""


def sort_questions_by_spacing(questions_list: list) -> list:
    """
    Sorts a list of question dictionaries using a spaced repetition strategy.
    Questions that have been answered incorrectly most often appear first,
    ensuring the user practises their weakest areas more frequently.

    Args:
        questions_list (list): List of question dictionaries from storage.

    Returns:
        list: The same list sorted in descending order of incorrect attempts.
    """
    return sorted(
        questions_list,
        key=lambda q: q.get("incorrect_attempts", 0),
        reverse=True
    )


def display_analytics_dashboard(user_object) -> None:
    """
    Prints a subject-by-subject performance breakdown for the given user.
    Flags any subject whose average score falls below 50 as needing review.

    Args:
        user_object (User): An instance of the User class from users.py.
    """
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
        if len(scores) == 0:
            continue  # skip subjects with no recorded scores

        average: float = sum(scores) / len(scores)
        print(f"   - {subject:<20} : {average:.1f}/100")

        if average < 50:
            # Alert the user that this subject needs extra attention
            print("     ⚠ Low performance detected. Review recommended.")

    print("=" * 45 + "\n")
