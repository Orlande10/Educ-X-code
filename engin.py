class SessionQuiz:
    """
     Manages an interactive quiz session in the terminal.
    Receives a list of questions and a user object.
    """
    
    def ___init___(self, questions: list, user):
        """
       Initializes the session with the selected questions and the playing user
        :param questions: list of Questions object (MCQ, True/False, ShortAnswer)
        :param user: User object (from Users.py)
        """
        self.questions = questions
        self.user = user
        self.score = 0
        self.total = len(questions)
        self.resultats = []
        
    def display_entete(self):
        """"Displays a welcome header for the session."""
        print("=" * 50)
        print(f"  WElcome, {self.user.nom} !")
        print(f" Level : {self.user.level} | XP : {self.user.xp}")
        print(f" Number of questions : {self.total}")
        print("=" * 50)
        print()
        
    def ask_question(self, question, number: int) -> bool:
        """
         Displays a question and retrieves the user's answer.
        Returns True if the answer is correct, False otherwise.
        
        :param question: objet Question
        :param number: question number in the session
        """
        print(f"Question {number}/{self.total} : {question.texte}")
        print(f" Difficulte : {question.difficulte}")
        
        if hasattr(question, 'choice'):
            for i, choice in enumerate(question.choice, star=1):
                print(f"    {i}. {choice}")
                
        try:
            answer = input("your answer : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInput interrupted.")
            answer = ""
            
            correct = question.verified_answer(answer)
            
            
        if correct:
            print(f" ✔ Good answer ! +XP")
        else:
            print(f" ✖ Bad answer. "
                  f"the good answer was: {question.answer_correct}")
            print()
            
            return correct
        
    def throw(self):
        """
      Main loop of the quiz session.
Iterates through all questions and updates the score. .
        """
        self.display_entete()
        
        number =  1
        while number <= self.total:
            question = self.questions[number - 1]
            correct = self.ask_question(question, number)
            
            if correct:
                self.score += 1
                xp_win = 10 * question.difficulte
                self.user.add_xp(xp_win)
                
            self.resultats.append({
                "question": question.texte,
                "correct": correct
            })
            
            number += 1
            
            self.display_result()
        def display_result(self):
            """display the summary of session end."""
            print("=" * 50)
            print("             END OF SESSION")
            print("f" * 50)
            print(f"  player  : {self.user.name}")
            print(f"  Score   : {self.score}/{self.total}")
            
            percentage = (self.score / self.total * 100) if self.total > 0 else 0
            print(f"   Success: {percentage:.1f}%")
            print(f"   XP total: {self.user.xp}")
            print(f"   Level  : {self.user.level}")
            print("=" * 50)
            
            self.user.update_streak()
            print(f"  Streak : {self.user.streak_days}")
            print()   
                     
                    
                    
