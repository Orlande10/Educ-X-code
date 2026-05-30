#===========================================================================
# utils.py - Spaced repetition and statistics management
# Project : Educ X | Author : Mahamadi | Module : Adaptive Engine & Analytics
#===========================================================================

def sort_questions_by_spacing(questions_list: list) -> list:
    """
    Sorts the questions to prioritize the ones with the most incorrect attempts.

    Args:
        questions_list (list): The list of question dictionaries from storage.

    Returns:
        list: The sorted list of questions in descending order of failures.
    """

    return sorted(
        questions_list, 
        key=lambda q: q.get("incorrect_attempts", 0), 
        reverse=True
    )


def display_analytics_dashboard(user_object) -> None:
    """
    Displays the calculated averages by subject and alerts for low scores.

    Args:
        user_object (User): The user profile instance from Doriane's module.
    """
    print("\n" + "=" * 45)
    print(f"   ACADEMIC ANALYTICS - {user_object.name.upper()}")
    print("=" * 45)
    
    history: dict = user_object.get_history()
    
    if not history:
        print("No performance data available yet.")
        print("=" * 45 + "\n")
        return

    print("Calculated averages by subject:")
    
    for subject, scores in history.items():
        if len(scores) == 0:
            continue
            
        average: float = sum(scores) / len(scores)
        
        print(f"-{subject:<20} : {average:.1f}/100")
        
        if average < 50:
            print("Low performance detected. Review recommended.")
            
    print("=" * 45 + "\n")