#===========================================================================
# Users.py - Gestion des profils utilisateurs et de la progression
# Projet : Educ X | Auteur : Doriane | Module : Utilisateur & Progression
#===========================================================================


#----Import----
from datetime import date,timedelta

#----constantes----
PALIERS_NIVEAU : tuple = (0, 100, 250, 500, 1000, 2000, 5000)
XP_PAR_DIFFICULTE: dict ={

    "facile": 10,
    "moyen": 20,
    "difficile": 35,
}
NIVEAU_MAX: int = len(PALIERS_NIVEAU) - 1

#==========================================================================
#CLASSE : Utilisateur
#==========================================================================

class Utilisateur:
    """
    Represente un etudiant utilisant l'application Educ X.
    Gere le profil,les points d'experience(XP), le niveau,le Streak de jours consecutifset l'historique des scores par matieres.
    """
    
    def __init__(self, nom: str) -> None:
        """
        Initialise un nouvel utilisateur
        Args:
        nom(str): Le nom de l'utilisateur.
        """
        self.nom: str=nom
        self.__xp: int=0                   #Encapsulation : attribut prive
        self.__niveau: int=1
        self.__streak_jours: int=0
        self.__derniere_connexion: date = date.today()
        
        #Dictionnaire:matiere: matiere ->liste de scores(historique)
        self.__historique_scores:dict = {}
        
        #---Getters (Abstraction :acces controlee aux aux donnees prives)---
        
    def get_xp(self) -> int:
            """Retourne le total de points xp de l'utilisateur."""
            return self.__xp
        
    def get_niveau(self) -> int:
            """Retourne le niveau actuel de l'utilisateur."""
            return self.__niveau   
        
    def get_streak(self) ->int:
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
        if points < 0:
             print("Erreur:Les points XP ne peuvent pas etre negatifs.")
             return
         
        self.__xp += points
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
                 self.__streak_jours = 1 
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
         
    def afficher_tableau_de_bord(self) -> None:
             """
             Affiche le tableau de bord complet de l'utilisateur :
             niveau, XP, streak, et moyennes par matiere.
             """
             print("\n" + "=" * 45)
             print(f"   TABLEAU DE BORD -{self.nom.upper()}")
             print("=" * 45)
             print(f"   Niveau     : {self.__niveau}")
             print(f" XP total     : {self.__xp} XP")
             print(f"Streak        : {self.__streak_jours} jour(s)")
             print("-" * 45)
             
             if not self.__historique_scores:
                 print("    Aucune session de quiz enregistree.")
             else:
                 print("Performances par matieres :")
                 for matiere, scores in self.__historique_scores.items():
                     moyenne: float = sum(scores)/len(scores)
                     print(f"    -{matiere:<20} Moy : {moyenne:.1f}/100  ({len(scores)} session(s))")
             print("=" * 45 + "\n")        
                     
    def identifier_points_faibles(self) -> list:
             """
             Identifie les matieres ou la moyenne est inferieure a 50/100.
             Returns:
             ist : Une liste de tuples(matiere,moyenne) pour les points faibles.
             
             """  
             Points_faibles: list = []
             
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
                 "xp":self.__xp,
                 "niveau":self.__niveau,
                 "streak_jours":self.__streak_jours,
                 "derniere_connexion": str(self.__derniere_connexion),
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
         #---Methode privee (Abstraction)---
    def __verifier_niveau(self) -> None:
             """
             Verifie si l'utilisateur a atteint un nouveau niveau selon ses XP .
             Methode privee appelee automatiquement apres chaque ajout de XP.
             """
             for i, palier in enumerate(PALIERS_NIVEAU):
                 if self.__xp >= palier:
                     nouveau_niveau: int = i + 1
                 else:
                     break
             nouveau_niveau = min(nouveau_niveau, NIVEAU_MAX)
             
             if nouveau_niveau > self.__niveau:
                 self.__niveau = nouveau_niveau
                 print(f"   NIVEAU SUPERIEUIR  ! TU es maintenant au niveau {self.__niveau}  !")
                 
    def __str__(self) -> str:
             """
             Retourne une representation lisible de l'utilisateur.
             """
             return (f"Utilisateur (nom={self.nom}, "
                    f"niveau={self.__niveau}, xp={self.__xp})")
         
         
#========================================================================================
#CLASSE ENFANT : UtilisateurPremium (Heritage + Polymorphysme)
#========================================================================================

class UtilisateurPremium(Utilisateur):
    """
    Version premium de l'utilisateur avec un multiplicateur de XP.
    Herite de Utilisateur et surcharge la methode  ajouter)_xp() 
    pour appliquer un bonus (polymorphysme).
    """
    MULTIPLICATEUR: float = 1.5
    def __init__(self, nom:str, abonnement: str) -> None:
        """
        Initialise un utilisateur premium.
        ARGS:
        nom(str):Le nom de l'utilisateur.
        abonnement(str): Le type d'abonnement(ex:"mensuel", "annuel").
        """
        super().__init__(nom)
        self.abonnement:str = abonnement
    def ajouter_xp(self, points: int) -> None:
        """
        Ajouter des XP avec un bonus de 50% par rapport a un utilisateur standard.
        Surcharge de la methode parente (polymorphisme).
        Args:
        points(int): Points XP de base a ajouter.
        """
        points_bonus: int = int(points * self.MULTIPLICATEUR)
        print(f" [Premium] Bonus XP appliquee : {points} -> {points_bonus} XP")
        super().ajouter_xp(points_bonus)
    def __str__(self) -> str:
        """
        Retourne une representation lisible de l'utilisateur premium.
        """
        return f"UtilisateurPremium(nom={self.nom}, abonnement={self.abonnement})"  
    
    
#==================================================================================
#TEST RAPIDE (A supprimer ou commenter avant la soussision finale)    
#==================================================================================

"""
if __name__=="__main__":
    #Creation de deux objetcts distincts (exigees par le brief) 
    etudiant1 =Utilisateur("Doriane")
    etudiant2 = UtilisateurPremium("Nelly", "mensuel")
    
    #Test des methodes
    etudiant1.mettre_a_jour_streak()
    etudiant1.ajouter_xp(120)
    etudiant1.enregistrer_score("Mathematiques", 72)
    etudiant1.enregistrer_score("Informatiques", 45)
    etudiant1.enregistrer_score("Mathematiques", 38)
    etudiant1.afficher_tableau_de_bord()
    
    #Identification des points faibles 
    faibles: list = etudiant1.identifier_points_faibles()
    if faibles:
        print("Points faibles detectes : ")
        for matiere, moy in faibles :
            print(f"   -{matiere} : {moy}/100")
    print()
    #Test polymorphisme
    etudiant2.ajouter_xp(100)
    print(etudiant2)    
"""    
