#===========================================================================
# users.py - user profile and progress management
# Project : Educ X | Author : Doriane | Module : User & Progress
#===========================================================================

from datetime import date, timedelta
from typing import Dict, List

LEVEL_THRESHOLDS = (0, 100, 250, 500, 1000, 2000, 5000)
XP_BY_DIFFICULTY = {
    "easy": 10,
    "medium": 20,
    "hard": 35,
}
MAX_LEVEL: int = len(LEVEL_THRESHOLDS) - 1

#==========================================================================
# CLASS : User
#==========================================================================

class User:
    """
    Represents a student using the Educ X application.
    Manages the user's profile, experience points (XP), level, streak of consecutive days,
    and score history by subject.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a new user.
        Args:
            name (str): The name of the user.
        """
        self.name: str = name
        self.__xp: int = 0
        self.__level: int = 1
        self.__streak_days: int = 0
        self.__last_login: date = date.today()
        self.__score_history: Dict[str, List[int]] = {}

    def get_xp(self) -> int:
        """Return the user's total XP points."""
        return self.__xp

    def get_streak(self) -> int:
        """Return the number of consecutive study days."""
        return self.__streak_days

    def get_history(self) -> dict:
        """Return the complete score history by subject."""
        return self.__score_history

    def add_xp(self, points: int) -> None:
        """
        Add XP points to the user and verify whether a level is reached.

        Args:
            points (int): The number of XP points to add.
        """
        if points < 0:
            print("Error: Points cannot be negative.")
            return

        self.__xp += points
        print(f"+{points} XP earned! Total: {self.__xp} XP")
        self.__verify_level()

    def update_streak(self) -> None:
        """
        Update the streak of consecutive study days.
        If the user logs in the day after their last login, the streak increases.
        Otherwise, it resets to 1.
        """
        today: date = date.today()
        yesterday: date = today - timedelta(days=1)

        if self.__last_login == yesterday:
            self.__streak_days += 1
            print(f"🔥 Streak maintained: {self.__streak_days} consecutive day(s)!")
        elif self.__last_login < yesterday:
            self.__streak_days = 1
            print("🔥 Streak reset. New start: 1 day.")
        else:
            print("Streak already updated today.")

        self.__last_login = today

    def record_score(self, subject: str, score: int) -> None:
        """
        Record a score for a given subject in the history.

        Args:
            subject (str): The subject name (example: "Mathematics").
            score (int): The score obtained (between 0 and 100).
        """
        if subject not in self.__score_history:
            self.__score_history[subject] = []

        self.__score_history[subject].append(score)
        print(f"Score recorded: {score}/100 in {subject}.")

    def display_dashboard(self) -> None:
        """
        Display the user's full dashboard:
        level, XP, streak, and averages by subject.
        """
        print("\n" + "=" * 45)
        print(f"   DASHBOARD - {self.name.upper()}")
        print("=" * 45)
        print(f"   Level      : {self.__level}")
        print(f"   Total XP   : {self.__xp} XP")
        print(f"   Streak     : {self.__streak_days} day(s)")
        print("-" * 45)

        if not self.__score_history:
            print("    No quiz sessions recorded.")
        else:
            print("Subject performance:")
            for subject, scores in self.__score_history.items():
                average: float = sum(scores) / len(scores)
                print(f"    - {subject:<20} Avg: {average:.1f}/100 ({len(scores)} session(s))")
        print("=" * 45 + "\n")

    def identify_weak_areas(self) -> list:
        """
        Identify subjects where the average is lower than 50/100.

        Returns:
            list: A list of tuples (subject, average) for weak areas.
        """
        weak_areas: list = []

        for subject, scores in self.__score_history.items():
            average: float = sum(scores) / len(scores)
            if average < 50:
                weak_areas.append((subject, round(average, 1)))

        return weak_areas

    def to_dict(self) -> dict:
        """
        Convert the user profile to a dictionary for JSON saving.

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
        Rebuild a user object from a dictionary containing profile data.

        Returns:
            User: The reconstructed user object.
        """
        user = cls(data["name"])
        user.__xp = data.get("xp", 0)
        user.__level = data.get("level", 1)
        user.__streak_days = data.get("streak_days", 0)
        user.__score_history = data.get("score_history", {})
        last = data.get("last_login", str(date.today()))
        user.__last_login = date.fromisoformat(last)
        return user

    def __verify_level(self) -> None:
        """
        Update the user's level based on total XP and predefined thresholds.
        """
        for i, threshold in enumerate(LEVEL_THRESHOLDS):
            if self.__xp < threshold:
                self.__level = max(1, i)
                return
        self.__level = MAX_LEVEL
         
         
             
                   
             
             
             
                          
                
                 
                     
                   
             
             
         