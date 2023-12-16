"""
 _____                                                      _____
( ___ )                                                    ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   |
 |   |                                                      |   |
 |   |      _____  _____  _______      __             _     |   |
 |   |     / ____||  __ \|__   __|    / _|           (_)    |   |
 |   |    | |  __ | |__) |  | |  ___ | |_  _ __  ___  _     |   |
 |   |    | | |_ ||  ___/   | | / _ \|  _|| '__|/ _ \| |    |   |
 |   |    | |__| || |       | ||  __/| |  | |  |  __/| |    |   |
 |   |     \_____||_|       |_| \___||_|  |_|   \___||_|    |   |
 |   |                                                      |   |
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___|
(_____)                                                    (_____)

GPTefrei est un ChatBot en Python réalisé par Eytan Guernigou et Tim Nguyen--Menu

Vous êtes actuelemnt dans le fichier main.py qui est le fichier d'exécution principale pour GptEfrei, si vous voulez utiliser GptEfrei il faut donc lancer main.py.
"""

from fonction import *
from affichage_demande import *

if __name__ == '__main__':

### Exécution de départ ###
    #_ L'exécution de départ comprend toutes les variables nécessaires au démarrage et au bon fonctionnement global du code. _#
    s_p_names = s_p_names("./speeches", ".txt")
    list_of_files = list_of_files("./speeches", ".txt")
    for file in list_of_files:
        clean_files(file)
    m_tf_idf, dic_files, dic_words = tf_idf(list_of_files, "cleaned")

    # création/clean d'un fichier qui fera office d'historique des questions posées durant une session. (rénisialisé a chaque début de session) #
    historique_question = open("historique_question.txt", "w", encoding="utf-8")
    historique_question.close()

### Menu ###
    #_ Le Menu comprend tout le code en rapport avec l'affichage utilisateur. _#
    print("""
 _____                                                      _____
( ___ )                                                    ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   |
 |   |                                                      |   |
 |   |      _____  _____  _______      __             _     |   |
 |   |     / ____||  __ \|__   __|    / _|           (_)    |   |
 |   |    | |  __ | |__) |  | |  ___ | |_  _ __  ___  _     |   |
 |   |    | | |_ ||  ___/   | | / _ \|  _|| '__|/ _ \| |    |   |
 |   |    | |__| || |       | ||  __/| |  | |  |  __/| |    |   |
 |   |     \_____||_|       |_| \___||_|  |_|   \___||_|    |   |
 |   |                                                      |   |
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___|
(_____)                                                    (_____)
GptEfrei. By Eytan Guernigou et Tim Nguyen--Menu.
    
Bonjour et bienvenue sur le tout-puissant GptEfrei, le chat-bot qui va révolutionner le monde et votre vie !
Voici toutes les fonctionnalités disponibles sur GptEfrei :""")

    fonctionnalite = 0
    while fonctionnalite != 4:

        print("""
1- Poser une question.
2- Afficher l'affichage demandé.
3- Afficher l'ensemble des fichiers de la base de données.
4- Quitter 
""")

        fonctionnalite = int(input("Pour accéder a l'une d'entre elles vous pouvez renseigné le numéro associer a la fonctionnaliser : "))
        while fonctionnalite < 1 or fonctionnalite > 4:
            fonctionnalite = int(input("Vous n'avez pas saisi un nombre correct, ressaisissez un nombre : "))


# Fonctionnalité 1, Question #
        if fonctionnalite == 1:
            print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       

Vous avez choisi la fonctionnalité de question/réponse.
Dans cette dernière vous pouvez poser une question et GptEfrei vous répondra en fonction. 
Il faut prendre en compte que les réponses renvoyer par GptEfrei sont proportionnellement précise en fonction du nombre de fichiers dans la base de données, ainsi si vous voulez des réponses plus précises il vous faut enrichir le dossier cleanned. """)

            choix = "question"
            while choix != "quitter":

                choix = str(input("""
Maintenant vous pouvez soit :
- Poser une question en écrivant 'question'. 
- Voire/Utiliser l'historique de vos questions en écrivant 'historique'. 
- Quittée en écrivant 'quitter'.
Que voulez-vous faire ? """))
                while choix != "question" and choix != "historique" and choix != "quitter":
                    choix = str(input("Votre choix est mauvais, pouvez-vous le réécrire : "))

                if choix == "question":
                    print("")
                    question = str(input("Maintenant vous pouvez poser votre question : "))
                    while question == "" or question == " ":
                        question = str(input("Votre question est incorecte, reposer votre question : "))

                    historique_question = open("historique_question.txt", "a", encoding="utf-8")
                    historique_question.write(question + "\n")
                    historique_question.close()

                    print("")
                    beautiful_awnser(awnser(m_tf_idf, dic_files, dic_words, list_of_files, question))
                    print("")

                elif choix == "historique":
                    print("")
                    historique_question = open("historique_question.txt", "r", encoding="utf-8")
                    questions = historique_question.readlines()
                    if questions == []:
                        print("Vous n'avez pas encore poser de question.")

                    else:
                        print("Vous avez posé ces question :")
                        for k in range(len(questions)):
                            print(f"{k+1}- {questions[k][:-1]}")

                        print("")
                        historique_choix = str(input("Voulez-vous reposer une question ? Oui/Non : "))
                        while historique_choix != "Oui" and historique_choix != "oui" and historique_choix != "Non" and historique_choix != "non":
                            historique_choix = str(input("Voulez-vous reposer une question ? Oui/Non : "))

                        if historique_choix == "Oui" or historique_choix == "oui":
                            historique_choix_question = int(input("Saisiser le numéro de la question que vous voulez reposer : "))
                            while historique_choix_question < 1 or historique_choix_question > (k+1):
                                historique_choix_question = int(input("Le numéro que vous avez saisi est incorect Veuillez le ressaisir : "))
                            print("")
                            beautiful_awnser(awnser(m_tf_idf, dic_files, dic_words, list_of_files, questions[historique_choix_question-1]))
                            print("")

            print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
""")


# Fonctionnalité 2, Affichage demander #
        elif fonctionnalite == 2:
            print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       

Vous avez choisi la fonctionnalité qui affiche l'affichage demandé. 
Dans cette dernière vous pouvez choisir une question et renseigner son numéro pour que les réponses à cette question soient affichées.""")

            choix = "affichage demande"
            while choix != "quitter":

                choix = str(input("""
Maintenant vous pouvez soit :
- Choisire la question a afficher en écrivant 'affichage demande'.
- Quittée en écrivant 'quitter'.
Que voulez-vous faire ? """))
                while choix != "affichage demande" and choix != "quitter":
                    choix = str(input("Votre choix est mauvais, pouvez-vous le réécrire : "))

                if choix == "affichage demande":
                    print("")
                    question_a_d = int(input("Il y a 6 questions dans l'affichage demandé, quelle question voulez-vous voir ? "))
                    while question_a_d < 1 or question_a_d > 6:
                        question_a_d = int(input("Le numéro de la question est incorecte, pouvez-vous la réécrire : "))

                    if question_a_d == 1:
                        print("")
                        affichage_demande_1(m_tf_idf, dic_words, list_of_files)
                    elif question_a_d == 2:
                        print("")
                        affichage_demande_2(m_tf_idf, dic_words, list_of_files)
                    elif question_a_d == 3:
                        print("")
                        affichage_demande_3(m_tf_idf, dic_words, list_of_files)
                    elif question_a_d == 4:
                        print("")
                        affichage_demande_4(m_tf_idf, dic_words, list_of_files)
                    elif question_a_d == 5:
                        print("")
                        affichage_demande_5(m_tf_idf, dic_words, list_of_files)
                    elif question_a_d == 6:
                        print("")
                        affichage_demande_6(m_tf_idf, dic_words, list_of_files)

            print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
""")


# Fonctionnalité 3, Base de données #
        elif fonctionnalite == 3:
            print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       

Vous avez choisi la fonctionnalité d'afficher tous les fichiers de la base de données de GptEfrei.""")

            choix = "base de données"
            while choix != "quitter":

                choix = str(input("""
Maintenant vous pouvez soit :
- Choisire d'afficher les fichers de la base de données en écrivant 'base de données'.
- Soit quittée en écrivant 'quitter'.
Que voulez-vous faire ? """))
                while choix != "base de données" and choix != "quitter":
                    choix = str(input("Votre choix est mauvais, pouvez-vous le réécrire : "))

                if choix == "base de données":
                    print("")
                    if list_of_files == []:
                        print("La base de données est vide.")
                    else:
                        for file in list_of_files:
                            print("-", file)

            print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
""")

    print("")
    print("Merci d'avoir utilisé GptEfrei.")