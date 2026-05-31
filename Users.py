"""
users.py
Defines the User and PremiumUser classes.
Manages player profiles, XP, levels, streaks, and score history by subject.
Demonstrates encapsulation, inheritance, and polymorphism.
"""

from datetime import date, timedelta

# XP thresholds required to reach each level (index = level - 1)
LEVEL_THRESHOLDS: tuple = (0, 100, 250, 500, 1000, 2000, 5000)

# XP awarded per question depending on its difficulty tag
XP_BY_DIFFICULTY: dict = {
    "easy":   10,
    "medium": 20,
    "hard":   35,
}

# The highest level a user can reach
MAX_LEVEL: int = len(LEVEL_THRESHOLDS) - 1


class User:
    """
    Represents a student using the Educ X application.
    Manages profile data, experience points (XP), level progression,
    daily streak tracking, and score history by subject.
    Encapsulation is applied: all progress data is stored as private attributes
    and accessed through getter methods.
    """

    def __init__(self, name: str) -> None:
        """
        Initialises a new User with default values.

        Args:
            name (str): The student's display name.
        """
        self.name: str = name
        self.__xp: int = 0                       # total XP points earned
        self.__level: int = 1                    # starts at level 1
        self.__streak_days: int = 0              # consecutive login days
        self.__last_login: date = date.today()   # used to track streak
        self.__score_history: dict = {}          # { subject: [score1, score2, ...] }

    # --- Getters: controlled access to private data (Abstraction) ---

    def get_xp(self) -> int:
        """Returns the user's total XP points."""
        return self.__xp

    def get_level(self) -> int:
        """Returns the user's current level."""
        return self.__level

    def get_streak(self) -> int:
        """Returns the number of consecutive study days."""
        return self.__streak_days

    def get_history(self) -> dict:
        """Returns the full score history dictionary, keyed by subject."""
        return self.__score_history

    # --- Core methods ---

    def add_xp(self, points: int) -> None:
        """
        Awards XP points to the user and triggers a level check.

        Args:
            points (int): Number of XP points to add. Must be non-negative.
        """
        if points < 0:
            print("Error: XP points cannot be negative.")
            return
        self.__xp += points
        print(f"+{points} XP earned! Total: {self.__xp} XP")
        self.__check_level()

    def update_streak(self) -> None:
        """
        Updates the daily study streak based on the last login date.
        Logging in the day after the last login increases the streak.
        Any longer gap resets it to 1.
        """
        today: date = date.today()
        yesterday: date = today - timedelta(days=1)

        if self.__last_login == yesterday:
            self.__streak_days += 1
            print(f"Streak maintained: {self.__streak_days} consecutive day(s)!")
        elif self.__last_login < yesterday:
            # More than one day has passed, streak is broken
            self.__streak_days = 1
            print("Streak reset. New start: 1 day.")
        else:
            # Already logged in today
            print("Streak already updated today.")

        self.__last_login = today

    def record_score(self, subject: str, score: int) -> None:
        """
        Records a quiz score for a given subject.

        Args:
            subject (str): The subject name, e.g. "Mathematics".
            score (int): The score to record, typically between 0 and 100.
        """
        if subject not in self.__score_history:
            self.__score_history[subject] = []
        self.__score_history[subject].append(score)
        print(f"Score recorded: {score}/100 in {subject}.")

    def display_dashboard(self) -> None:
        """
        Prints a summary dashboard showing the user's level, XP,
        streak, and average scores per subject.
        """
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
        """
        Finds subjects where the user's average score is below 50.

        Returns:
            list: A list of tuples (subject, average) for weak subjects.
        """
        weak_points: list = []
        for subject, scores in self.__score_history.items():
            average: float = sum(scores) / len(scores)
            if average < 50:
                # Store as an immutable tuple: (subject name, rounded average)
                weak_points.append((subject, round(average, 1)))
        return weak_points

    def to_dict(self) -> dict:
        """
        Converts the user profile into a serialisable dictionary for JSON storage.

        Returns:
            dict: All user data in a JSON-compatible format.
        """
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
        """
        Reconstructs a User object from a saved dictionary.

        Args:
            data (dict): Dictionary as loaded from the JSON file.

        Returns:
            User: A fully restored User instance.
        """
        user = cls(data["name"])
        user._User__xp = data.get("xp", 0)
        user._User__level = data.get("level", 1)
        user._User__streak_days = data.get("streak_days", 0)
        user._User__score_history = data.get("score_history", {})
        last_login = data.get("last_login", str(date.today()))
        user._User__last_login = date.fromisoformat(last_login)
        return user

    def __check_level(self) -> None:
        """
        Checks whether the current XP total qualifies for a higher level.
        Called automatically after every XP award.
        """
        new_level: int = 1
        for i, threshold in enumerate(LEVEL_THRESHOLDS):
            if self.__xp >= threshold:
                new_level = i + 1
            else:
                break  # stop as soon as we fall below a threshold

        new_level = min(new_level, MAX_LEVEL)

        if new_level > self.__level:
            self.__level = new_level
            print(f" LEVEL UP! You are now level {self.__level}!")

    def __str__(self) -> str:
        """Returns a human-readable summary of the user."""
        return f"User(name={self.name}, level={self.__level}, xp={self.__xp})"


class PremiumUser(User):
    """
    A premium student who earns 50% more XP per correct answer.
    Inherits all behaviour from User and overrides add_xp() to apply the bonus.
    Demonstrates inheritance and polymorphism: same method name, different behaviour.
    """

    XP_MULTIPLIER: float = 1.5  # premium users earn 1.5x XP

    def __init__(self, name: str, subscription: str) -> None:
        """
        Initialises a PremiumUser.

        Args:
            name (str): The student's display name.
            subscription (str): Subscription type, e.g. "monthly" or "yearly".
        """
        super().__init__(name)
        self.subscription: str = subscription

    def add_xp(self, points: int) -> None:
        """
        Awards XP with a 50% bonus applied before calling the parent method.
        Overrides User.add_xp() — this is polymorphism in action.

        Args:
            points (int): Base XP points before the premium multiplier is applied.
        """
        bonus_points: int = int(points * self.XP_MULTIPLIER)
        print(f"[Premium] XP bonus applied: {points} -> {bonus_points} XP")
        super().add_xp(bonus_points)

    def __str__(self) -> str:
        """Returns a human-readable summary of the premium user."""
        return f"PremiumUser(name={self.name}, subscription={self.subscription})"
