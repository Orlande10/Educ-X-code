#===========================================================================
# Users.py - User Profile and Progress Management
# Project: Educ X | Author: Doriane | Module: User & Progress
#===========================================================================


#----Import----
from datetime import date, timedelta

#----Constants----
LEVEL_THRESHOLDS: tuple = (0, 100, 250, 500, 1000, 2000, 5000)

XP_BY_DIFFICULTY: dict = {
    "easy": 10,
    "medium": 20,
    "hard": 35,
}

MAX_LEVEL: int = len(LEVEL_THRESHOLDS) - 1

#==========================================================================
#CLASS: User
#==========================================================================

class User:
    """
    Represents a student using the Educ X application.
    Manages the profile, experience points (XP), level,
    consecutive-day streak, and score history by subject.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a new user.

        Args:
        name(str): The user's name.
        """
        self.name: str = name
        self.__xp: int = 0                  # Encapsulation: private attribute
        self.__level: int = 1
        self.__streak_days: int = 0
        self.__last_login: date = date.today()

        # Dictionary: subject -> list of scores (history)
        self.__score_history: dict = {}

        #---Getters (Abstraction: controlled access to private data)---

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
        """Returns the complete score history by subject."""
        return self.__score_history

    #---Main Methods---

    def add_xp(self, points: int) -> None:
        """
        Adds XP points to the user and checks whether a new level is reached.

        Args:
            points(int): The number of XP points to add.
        """
        if points < 0:
            print("Error: XP points cannot be negative.")
            return

        self.__xp += points
        print(f"+{points} XP earned! Total: {self.__xp} XP")
        self.__check_level()

    def update_streak(self) -> None:
        """
        Updates the consecutive study-day streak.

        If the user logs in the day after their last login,
        the streak increases. Otherwise, it is reset to 1.
        """
        today: date = date.today()
        yesterday: date = today - timedelta(days=1)

        if self.__last_login == yesterday:
            self.__streak_days += 1
            print(f"🔥Streak maintained: {self.__streak_days} consecutive day(s)!")
        elif self.__last_login < yesterday:
            self.__streak_days = 1
            print("🔥Streak reset. New start: 1 day.")
        else:
            # Same-day login, nothing to do
            print("Streak already updated today.")

        self.__last_login = today

    def record_score(self, subject: str, score: int) -> None:
        """
        Records a score for a given subject in the history.

        Args:
        subject(str): The subject name (e.g. Mathematics).
        score(int): The score obtained (between 0 and 100).
        """
        if subject not in self.__score_history:
            self.__score_history[subject] = []

        self.__score_history[subject].append(score)
        print(f"Score recorded: {score}/100 in {subject}.")

    def display_dashboard(self) -> None:
        """
        Displays the complete user dashboard:
        level, XP, streak, and subject averages.
        """
        print("\n" + "=" * 45)
        print(f"   DASHBOARD - {self.name.upper()}")
        print("=" * 45)
        print(f"   Level      : {self.__level}")
        print(f" Total XP     : {self.__xp} XP")
        print(f" Streak       : {self.__streak_days} day(s)")
        print("-" * 45)

        if not self.__score_history:
            print("No quiz sessions recorded.")
        else:
            print("Performance by subject:")
            for subject, scores in self.__score_history.items():
                average: float = sum(scores) / len(scores)
                print(
                    f" - {subject:<20} Avg: {average:.1f}/100 ({len(scores)} session(s))"
                )

        print("=" * 45 + "\n")

    def identify_weak_points(self) -> list:
        """
        Identifies subjects whose average score is below 50/100.

        Returns:
        list: A list of tuples (subject, average) representing weak points.
        """
        weak_points: list = []

        for subject, scores in self.__score_history.items():
            average: float = sum(scores) / len(scores)

            if average < 50:
                            # Immutable tuples (subject, rounded average)
                            weak_points.append((subject, round(average, 1)))

        return weak_points

    def to_dict(self) -> dict:
        """
        Converts the user profile into a dictionary for JSON storage.

        Returns:
        dict: Serializable representation of the user profile.
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
        Reconstructs a user object from a dictionary containing profile data.

        Returns:
        User: The reconstructed user object.
        """
        user = cls(data["name"])
        user.User__xp = data.get("xp", 0)
        user.User__level = data.get("level", 1)
        user.User__streak_days = data.get("streak_days", 0)
        user.User__score_history = data.get("score_history", {})

        last_login = data.get("last_login", str(date.today()))
        user.User__last_login = date.fromisoformat(last_login)

        return user

    #---Private Method (Abstraction)---

    def __check_level(self) -> None:
        """
        Checks whether the user has reached a new level based on XP.
        Private method automatically called after each XP addition.
        """
        for i, threshold in enumerate(LEVEL_THRESHOLDS):
            if self.__xp >= threshold:
                new_level: int = i + 1
            else:
                break

        new_level = min(new_level, MAX_LEVEL)

        if new_level > self.__level:
            self.__level = new_level
            print(f"🎉 LEVEL UP! You are now level {self.__level}!")

    def __str__(self) -> str:
        """
        Returns a readable representation of the user.
        """
        return (
            f"User(name={self.name}, "
            f"level={self.__level}, xp={self.__xp})"
        )


#========================================================================================
#CHILD CLASS: PremiumUser (Inheritance + Polymorphism)
#========================================================================================

class PremiumUser(User):
    """
    Premium version of a user with an XP multiplier.

    Inherits from User and overrides the add_xp()
    method to apply a bonus (polymorphism).
    """

    XP_MULTIPLIER: float = 1.5

    def __init__(self, name: str, subscription: str) -> None:
        """
        Initializes a premium user.

        Args:
        name(str): The user's name.
        subscription(str): Subscription type (e.g. "monthly", "yearly").
        """
        super().__init__(name)
        self.subscription: str = subscription

    def add_xp(self, points: int) -> None:
        """
        Adds XP with a 50% bonus compared to a standard user.

        Overrides the parent method (polymorphism).

        Args:
        points(int): Base XP points to add.
        """
        bonus_points: int = int(points * self.XP_MULTIPLIER)

        print(
            f"[Premium] XP bonus applied: "
            f"{points} -> {bonus_points} XP"
        )

        super().add_xp(bonus_points)

    def __str__(self) -> str:
        """
        Returns a readable representation of the premium user.
        """
        return (
            f"PremiumUser("
            f"name={self.name}, "
            f"subscription={self.subscription})"
        )


#==================================================================================
#QUICK TEST (Remove or comment out before final submission)
#==================================================================================

if __name__ == "__main__":

    # Creation of two distinct objects (required by the project brief)
    student1 = User("Doriane")
    student2 = PremiumUser("Nelly", "monthly")

    # Method tests
    student1.update_streak()
    student1.add_xp(120)

    student1.record_score("Mathematics", 72)
    student1.record_score("Computer Science", 45)
    student1.record_score("Mathematics", 38)

    student1.display_dashboard()

    # Weak point identification
    weak_points: list = student1.identify_weak_points()

    if weak_points:
        print("Weak points detected:")

        for subject, average in weak_points:
            print(f"   - {subject}: {average}/100")

    print()

    # Polymorphism test
    student2.add_xp(100)
    print(student2)