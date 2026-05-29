#===========================================================================
# Users.py - Gestion des profils utilisateurs et de la progression
# Projet : Educ X | Auteur : Doriane | Module : Utilisateur & Progression
#===========================================================================


#----Import----
from datetime import date,timedelta

#----onstante----
PALIERS_NIVEAU : tuple(0, 100, 250, 500, 1000, 2000, 5000)
XP_PAR_DIFFICULTE: dict
{
    "facile":10;
    "moyen":20;
    "difficile": 35;
}
Niveau_MAX: int=len(PALIERS_NIVEAU)-1

#==========================================================================
#CLASSE : Utilisateur
#==========================================================================

class Utilisateur:
    """
    Represente un etudiant utilisant l'application Educ X.
    Gere le profil,les points d'experience(XP), le niveau,le Streak de jours consecutifset l'historique des scores par matieres.
    """
    def__init__(self,nom:str) -> None:
        """
        Initialise un nouvel utilisateur
        Args:
        nom(str): Le nom de l'utilisateur.
        """
        self.nom:str=nom
        self.__xp:int=0                   #Encapsulation : attribut prive
        self.__niveau: int=1
        self.__streak_jours: int=0
        self.__derniere_connexion: date=date.today()
        
        #Dictionnaire:matiere: matiere ->liste de3 scores(historique)
        self.__historique_score:dict={}
        
        #---Getters (Abstraction :acces controlee aux aux donnees prives)---
        
        def get_niveau(self) -> int:
            """Retourne le total de points xp de l'utilisateur."""
            return self.__xp
        
        def get_NIVEAU(self) ->int:
            """Retourne  le nombre de jours consecutifs de revisions."""
            return self.__streak_jours
        
        def get_historique(self) -> dict:
            """Retourne l'historique complet des scores par matieres"""
            return self.__historique_scores
         
         #---Methodes principales---
         
         def ajouter_xp(self,points: int) -> None:
         """
         Ajouter des points XP a l'utilisateur et verifier si un niveau est atteint.
         
         Args:
         points(int): Le nombre de points XP a ajouter.
         """
         if points<0:
             print("Erreur:Les points ne peuvent pas etre negatifs.")
             return
         
         self.__xp +=points
         print(f" +{points} XP gagnes ! Total : {self.__xp} XP")
         self.__verifier_niveau()
         
         def mettre_a_jour_streak(self) -> None:
             """
             Met a jour le streak de jours consecutifs de revisions.
             
             Si l'utilisateur se connecte le jour suivant sa derniere connexion,
             le streak augmente.Sinon ,il est reinitialise a 1.
             """
             aujourd_hui: date = date.today()
             hier: date = aujourd_hui - timedelta(days=1)
             
             if self.__derniere_connexion == hier:
                 self.__streak_jours +=1
                 print(f"🔥Streak maintenu : {self.__streak_jours} jours consecutif(s)!")
             elif self.__derniere_connexion<hier:
                 self.streak_jours = 1 
                 print(f"🔥Streak renitialise .Nouveau depart : 1 jour.")
             else:
                 #connexion le meme jour,on ne fait rien
                 print(" Streak deja mis a jour aujourd'hui.")   
             self.__derniere_connexion = aujourd_hui
             
         def enregistrer_score(self, matiere: str,score: int) -> None:
             """
             Enregistre un score pour une matiere donnee dans l'historique.
             
             Args:
             matiere(str): Le nom de la matiere(ex:"Mathematiques).
             score(int): Le score obtenu(Entre 0 et 100).
             """
             if matiere not in self.__historique_scores:
                 self.__historique_scores[matiere] = []
             
             self.__historique_scores[matiere].append(score)
             print(f" Score enregistre : {score}/100 en {matiere}.")
         
         def afficher_tableau_de_bord(saelf) -> None:
             """
             Affiche le tableau de bord complet de l'utilisateur :
             niveau, XP, streak, et moyennes par matiere.
             """
             print("\n" + "=" * 45)
             print(f"   TABLEAU DE BORD -{self.nom.upper()}")
             print("=" * 45)
             print(f"   Niveau     : {self.__niveasu}")
             print(f" XP total     : {self.__xp} XP")
             print(f"Streak        : {self.__streak_jours} jour(s)")
             print("-" * 45)
             
             if not self.__historique_scores:
                 print("    Aucune session de quiz enregistree.")
             else:
                 print("Performances par matieres :")
                 for matiere, scores in self.___historique_scores.items():
                     moyenne: float = sum(scores)/len(scores)
                     print(f"    -{matiere:<20} Moy : {moyenne:.1f}/100  ({len(scores)} session(s))")
             print("=" * 45 + "\n")        
                     
         def identifier_points_faibles(self) -> list:
             """
             Identifie les matieres ou la moyenne est inferieure a 50/100.
             Returns:
             ist : Une liste de tuples(matiere,moyenne) pour les points faibles.
             
             """  
             Points_faibles: list[]
             
             for matiere, scores in self.__historique_scores.items():
                 moyenne : float = sum(scores) / len(scores)
                 if moyenne < 50 :
                     #Tuples immuables (matieres, moyenne arrondie)
                     Points_faibles.append((matiere, round(moyenne, 1)))
                     
             return Points_faibles  
         def to_dict(self) -> dict:
             """
             Converti le profil utilisateur en dictionnaire pour la sauvegarde de JSON.
             
             Returns:
             dict:Representation serialisable du profil utilisateur.
             """
             return{
                 "nom": self.nom,
                 "xp":self._xp,
                 "niveau":self.__niveau,
                 "streak_jours":self.__streak_jours,
                 "derniere_connexion": str(self._derniere_connexion),
                 "historique_scores": self.__historique_scores,
             }
         @classmethod
         def from_dict(cls, data: dict) -> "Utilisateur":
             """
             Reconstruit un objet utilisateur a partir d'un dictionnaire contenant es donnees du profil.
             Returns:
             Utilisateurs : L'objet utilisateur reconstruit.
             """
             utilisateur = cls(data["nom"])
             utilisateur.Utilisateur__xp = data.get("xp", 0)
             utilisateur.Utilisateur__niveau = data.get("niveau", 1)
             utilisateur.Utilisateur__streak_jours = data.get("streak_jours", 0)
             utilisateur.Utilisateur__historique_scores = data.get("historique_scores", {})
             derniere = data.get("derniere_connexion", str(date.today()))
             utilisateur.Utilisateur__derniere_connexion = date.fromisoformat(derniere)
             return utilisateur
         #Methode privee (Abstraction)
         
         
         
             
                   
             
             
             
                          
                
                 
                     
                   
             
             
         