class SessionQuiz:
    """
    Gere une session interactive de quiz dans le terminal.
    recoit une liste de questions et un objet utilisateur.
    """
    
    def ___init___(self, questions: list, utilisateur):
        """
        Initialise la session avec les questions selectionnees et l,utilisateur qui joue.
        
        :param questions: liste d,objets Question (QCM, Vrai/Faux, ReponseCourte)
        :param utilisateur: object Utilisateur (depuis users.py)
        """
        self.questions = questions
        self.utilisateur = utilisateur
        self.score = 0
        self.total = len(questions)
        self.resultats = []
        
    def afficher_entete(self):
        """Affiche un en-tete de bienvenue pour la session."""
        print("=" * 50)
        print(f"  Bienvenue, {self.utilisateur.nom} !")
        print(f" Niveau : {self.utilisateur.niveau} | XP : {self.utilisateur.xp}")
        print(f" Nombre de questions : {self.total}")
        print("=" * 50)
        print()
        
    def poser_question(self, question, numero: int) -> bool:
        """
        Afficher une question et recupere la reponse de l,utilisateur.
        Retourne True si la reponseest correcte, False sinon.
        
        :param question: objet Question
        :param numero: numero de la dans la session
        """
        print(f"Question {numero}/{self.total} : {question.texte}")
        print(f" Difficulte : {question.difficulte}")
        
        if hasattr(question, 'choix'):
            for i, choix in enumerate(question.choix, star=1):
                print(f"    {i}. {choix}")
                
        try:
            reponse = input("Votre reponse : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaisie interrompue.")
            reponse = ""
            
            correct = question.verifier_reponse(reponse)
            
            
        if correct:
            print(f" ✔ Bonne reponse ! +XP")
        else:
            print(f" ✖ Mauvaise reponse. "
                  f"La bonne reponse etait : {question.reponse_correcte}")
            print()
            
            return correct
        
    def lancer(self):
        """
        Boucle principale de la session de quiz.
        Parcourt toutes les questions et met a jour le score.
        """
        self.afficher_entete()
        
        numero =  1
        while numero <= self.total:
            question = self.questions[numero - 1]
            correct = self.poser_question(question, numero)
            
            if correct:
                self.score += 1
                xp_gagne = 10 * question.difficulte
                self.utilisateur.ajouter_xp(xp_gagne)
                
            self.resultats.append({
                "question": question.texte,
                "correct": correct
            })
            
            numero += 1
            
            self.afficher_bilan()
        def afficher_bilan(self):
            """Afficher le resume de fin de session."""
            print("=" * 50)
            print("             FIN DE LA SESSION")
            print("f" * 50)
            print(f"  Joueur  : {self.utilisateur.nom}")
            print(f"  Score   : {self.score}/{self.total}")
            
            pourcentage = (self.score / self.total * 100) if self.total > 0 else 0
            print(f"   Reussite: {pourcentage:.1f}%")
            print(f"   XP total: {self.utilisateur.xp}")
            print(f"   Niveau  : {self.utilisateur.niveau}")
            print("=" * 50)
            
            self.utilisateur.mettre_a_jour_streak()
            print(f"  Streak : {self.utilisateur.streak_jours}")
            print()   
                     
                    
                    