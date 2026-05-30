#===========================================================================
# Users.py - user profile and progress management 
# Project : Educ X | Author : Doriane | Module : User & Progress
#===========================================================================


#----Import----     
from datetime import date, timedelta
from os import name

#----Constante----
LEVEL_THRESHOLDS: tuple = (0, 100, 250, 500, 1000, 2000, 5000)
XP_PER_DIFFICULTY: dict = {
    "easy": 10,
    "medium": 20,
    "hard": 35
}
LEVEL_MAX: int = len(LEVEL_THRESHOLDS) - 1

#==========================================================================
#CLASS : User
#==========================================================================

class User:
    """
    Represents a student using the Educ X application.
    Manages the user's profile, experience points (XP), level, streak of consecutive days, and score history by subject.
    """
    def __init__(self, name: str) -> None:
        """
        Initialize a new user
        Args:
            name(str): The name of the user.
        """
        self.name: str = name
        self.__xp: int = 0                   # Encapsulation : attribut prive
        self.__level: int = 1
        self.__streak_days: int = 0
        self.__last_login: date = date.today()
        
        # Dictionary: matter -> list of scores (historical scores for each subject)
        self.__historical_score: dict = {}

    #---Getters (Abstraction: access control to private data)---

    def get_xp(self) -> int:
        """Returns the total experience points of the user."""
        return self.__xp
    
    def get_level(self) -> int:
        """Returns the user's current level."""
        return self.__level
    
    def get_streak_days(self) -> int:
        """Returns the number of consecutive days of revisions."""
        return self.__streak_days
    
    def get_historical_scores(self) -> dict:
        """Returns the complete score history by subjects."""
        return self.__historical_score

    #---Main Methods---

    def add_xp(self, points: int) -> None:
        """
        Add experience points to the user and check if a new level is reached.
        
        Args:
            points(int): The number of XP points to add.
        """
        if points < 0:
            print("Error: Points cannot be negative.")
            return
        
        self.__xp += points
        print(f" +{points} XP gagnes ! Total : {self.__xp} XP")
        self.__verified_level()

    def update_streak(self) -> None:
        """
        Updates the streak of consecutive days.
        
        If the user logs in the day after their last login,
        the streak increases. Otherwise, it is reset to 1.
        """
        today: date = date.today()
        yesterday: date = today - timedelta(days=1)
        
        if self.__last_login == yesterday:
            self.__streak_days += 1
            print(f"🔥 Streak maintained: {self.__streak_days} consecutive day(s)!")
        elif self.__last_login < yesterday:
            self.__streak_days = 1 
            print(f"🔥 Streak reset. New starting: 1 day.")
        else:
            # Same day connection, we do nothing
            print("Streak already updated today.")   
        self.__last_login = today

    def save_score(self, matter: str, score: int) -> None:
        """
        Saves the score obtained by the user for a quiz in a specific subject.
        
        Args:
            matter(str): The name of the subject (e.g., "Mathematics").
            score(int): The score obtained (between 0 and 100).
        """
        if not isinstance(score, int) or score < 0 or score > 100:
            print("Error: Score must be an integer between 0 and 100.")
            return
        
        if matter not in self.__historical_score:
            self.__historical_score[matter] = []
        
        self.__historical_score[matter].append(score)
        print(f"Score recorded: {score}/100 in {matter}.")

    def display_dashboard(self) -> None:
        """
        Displays the complete dashboard of the user:
        level, XP, streak, and averages by subject.
        """
        print("\n" + "=" * 45)
        print(f"   Dashboard - {self.name.upper()}")
        print("=" * 45)
        print(f"   Level     : {self.__level}")
        print(f"   Total XP  : {self.__xp} XP")
        print(f"   Streak    : {self.__streak_days} day(s)")
        print("-" * 45)
        
        if not self.__historical_score:
            print("   No quiz sessions recorded.")
        else:
            print("   Performances by subjects:")
            for matter, scores in self.__historical_score.items():
                moyenne: float = sum(scores) / len(scores)
                print(f"    - {matter:<20} Avg: {moyenne:.1f}/100  ({len(scores)} session(s))")
        print("=" * 45 + "\n")

    def identify_weak_points(self) -> list:
        """
        Identifies the subjects where the average score is below 50/100.
        
        Returns:
            list: A list of tuples (subject, average) for the weak points.
        """  
        weak_points: list = []
        
        for matter, scores in self.__historical_score.items():
            if len(scores) > 0:
                average: float = sum(scores) / len(scores)
                if average < 50:
                    # Tuples immuables (matieres, moyenne arrondie)
                    weak_points.append((matter, round(average, 1)))
        
        return weak_points

    def to_dict(self) -> dict:
        """
        Converts the user profile to a dictionary for JSON serialization.
        
        Returns:
            dict: A serializable representation of the user profile.
        """
        return {
            "name": self.name,
            "xp": self.__xp,
            "level": self.__level,
            "streak_days": self.__streak_days,
            "last_login": str(self.__last_login),
            "historical_scores": self.__historical_score,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """
        Reconstructs a user object from a dictionary containing the profile data.
        
        Returns:
            user: User object reconstructed from the provided data.
        """
        user = cls(data["name"])
        user._User__xp = data.get("xp", 0)
        user._User__level = data.get("level", 1)
        user._User__streak_days = data.get("streak_days", 0)
        user._User__historical_score = data.get("historical_scores", {})
        last_login = data.get("last_login", str(date.today()))
        user._User__last_login = date.fromisoformat(last_login)
        return user

    #---Private Methods (Abstraction)---

    def __verified_level(self) -> None:
        """
        Verifies if the user has reached a new level based on current XP.
        Automatically updates the level when XP threshold is exceeded.
        """
        for level in range(1, LEVEL_MAX + 1):
            if self.__xp >= LEVEL_THRESHOLDS[level]:
                if self.__level < level:
                    self.__level = level
                    print(f"🎉 Congratulations! You reached level {self.__level}!")
            else:
                break
