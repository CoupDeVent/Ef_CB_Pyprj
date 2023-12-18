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

Vous êtes actuelemnt dans le fichier fonction.py qui est le fichier contenant toute les fonctions nécessaires au bon fonctionnement de GptEfrei.
"""
### import ###


import os
import math

# import pour la beauté des réponses (menu) #
from random import uniform
from time import sleep


### Fonctions de base ###

def list_of_files(directory, extension):
    """
    list_of_files : liste tous les noms de fichier dans un dossier.
    - Entrées : directory = dossier des fichiers a listés.
                extension = l'extension commune de tous les fichiers.
    - Sortie : files_names = une liste de tous les noms des fichiers listés.
    """
    files_names = []

    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)

    return files_names

def s_p_names(directory, extension):
    """
        s_p_names : donne tous les noms des présidents grâce a un dossier spécifié en entrée en suivant la logique de nomination des fichiers speeches.
        - Entrées : directory = dossier des fichiers.
                    extension = l'extension commune de tous les fichiers.
        - Sortie : p_names = une liste de tous les prénoms et noms des président du dossier.
        /!\ : tous les fichiers du dossier doivent suivre une nomination spécifique.
    """
    p_f_names = {
        "Giscard dEstaing": "Valéry",
        "Chirac": "Jacques",
        "Mitterrand": "François",
        "Macron": "Emmanuel",
        "Sarkozy": "Nicolas",
        "Hollande": "François"
    }
    files_names = list_of_files(directory, extension)
    p_names = []

    for file in files_names:
        name = file[11:(len(file))-4]
        while (ord(name[len(name)-1]) >= 48) and (ord(name[len(name)-1]) <= 57): # enlève les nombres a la fin des nom tant qu'il y en a.
            name = name[:len(name)-1]
        if p_f_names[name] + " " + name not in p_names:
            p_names.append(p_f_names[name] + " " + name)

    return p_names


def clean_files(file_name):
    """
        clean_files : clean le fichier donné en entrée de toutes ses : majuscule(s), marque(s) de ponctuation, espace(s) supérieur(s) à 1 et saut de ligne. (fichier ouvert en utf-8)
        - Entrées : file_name = nom du fichier à clean.
        - Sortie : créer/modifie un fichier du même nom dans un dossier "cleaned" avec les modifications.
        /!\ : nécésite un dossier "cleaned" créé au préalable.
        /!\ : si fichier déjà présent dans le dossier "cleaned" alors son contenu sera écrasé.
    """
    with open("speeches/"+file_name, "r", encoding="utf-8") as file, open("cleaned/"+file_name, "w", encoding="utf-8") as file_clean:
        f_content = file.read()
        new_content = ""
        word = ""
        for carac in (f_content + " "):
            if (ord(carac) >= 65 and ord(carac) <= 90) or (ord(carac) >= 192 and ord(carac) <= 223):
                word += chr(ord(carac)+32)
            elif (ord(carac) >= 97 and ord(carac) <= 122) or (ord(carac) >= 224 and ord(carac) <= 255):
                word += carac
            elif word != "":
                new_content += word + " "
                word = ""
        file_clean.write(new_content)


### TF-IDF ###


def tf(file_name, case):
    """
        tf : Donne la fréquence d'un terme dans un fichier.
        - Entrées : file_name = nom du fichier a tf-idéiser.
                    case = nom du dossier du fichier.
        - Sortie : dic_of_words = un dictionnaire de tous les mots du fichier avec leurs fréquences.
    """
    if case != "":
        case += "/"

    with open(case+file_name, "r", encoding="utf-8") as file:
        f_content = file.read()
        dic_of_words = {}

        for word in f_content.split(" "):
                if word in dic_of_words:
                    dic_of_words[word] += 1
                elif word != "":
                    dic_of_words[word] = 1

        return dic_of_words

def idf(list_of_files, case):
    """
        idf : Calcule le score IDF (log((nb_fichier/nb_fichier_mot) + 1)) de chaque mot dans un dictionnaire.
        - Entrées : list_of_files = liste de nom de fichier.
                    case = nom du dossier des fichier.
        - Sortie : idf_dic = un dictionnaire de tous les scores IDF de tout les mots de tous les fichiers de la liste de noms de fichiers donnés en entrée.
    """
    words_of_files = {}
    idf_dic = {}

    for file in list_of_files:
        dic = tf(file, case)
        for key in dic:
            if key in words_of_files:
                words_of_files[key] += 1
            else:
                words_of_files[key] = 1

    for key in words_of_files:
        idf_dic[key] = math.log10((len(list_of_files)/words_of_files[key])) # calcule du score idf : log((nb_fichier/mot))

    return idf_dic

def tf_idf(list_of_files, case):
    """
        tf_idf : Calcule le score TF-IDF grâce aux deux dictionnaires donnés par les deux fonctions ("tf" et "idf").
        - Entrées : list_of_files = liste de nom de fichier.
                    case = nom du dossier des fichiers.
        - Sortie : m_tf_idf = une matrice des vecteurs TF-IDF (colonne = fichier, ligne = mot)
                   dic_files = un dictionnaire des fichiers (key = nom du fichier, valeur = index (colonne) des fichiers dans la matrice "m_tf_idf")
                   dic_words = un dictionnaire des mots (key = mots, valeur = index (colonne) des mots dans la matrice"m_tf_idf")
        /!\ la sortie des 3 variable se fait en tuple.
    """
    idf_dic = idf(list_of_files, case)
    m_tf_idf = [[0.0 for k in range(len(list_of_files))] for i in range(len(idf_dic))] # création d'un tableau de "len(list_of_files)" lignes et de "len(idf_dic)" colonnes.
    dic_files = {file: k for file, k in zip(list_of_files, range(len(list_of_files)))} # création d'un dictionnaire de key = "file" dans "list_of_files" et valeur = "k" = compteur de longueur de "list_of_file".
    dic_words = {word: k for word, k in zip(idf_dic, range(len(idf_dic)))} # création d'un dictionnaire de key = "word" dans "idf_dic" et valeur = "k" = compteur de longueur de "idf_dic".

    for file in list_of_files:
        tf_dic = tf(file, case)
        for word in tf_dic:
            m_tf_idf[dic_words[word]][dic_files[file]] = tf_dic[word] * idf_dic[word] # calcule vecteur TF-IDF a l'emplacement du mot dans la matrice (ligne = valeur du mot dans le dictionnaire "dic_words", colonne = valeur du nom du fichier dans le dictionnaire "dic_files").

    return (m_tf_idf, dic_files, dic_words) # tuple


### Partie II, Réponses aux questions. ###


def tok(question):
    """
    tok : toketis une chaîne de caractères à l'instar de la fonction "clean_files" qui clean un fichier.
    - Entrées : question = une chaîne de caractère.
    - Sortie : words = une liste de tous les mots "clean" de la chaîne de caractères donnés en entrée.
    """
    words = []
    word = ""

    for carac in (question + " "):
        if (ord(carac) >= 65 and ord(carac) <= 90) or (ord(carac) >= 192 and ord(carac) <= 223):
            word += chr(ord(carac) + 32)
        elif (ord(carac) >= 97 and ord(carac) <= 122) or (ord(carac) >= 224 and ord(carac) <= 255):
            word += carac
        elif word != "":
            words.append(word)
            word = ""

    return words

"""
fonction demandée dans le pdf de la partie II et III mais non utilisée dans le code.
def question_in_corp(m_tf_idf, dic_words, question):
    question = tok(question)
    result = []

    for word in dic_words:
        if word in question:
            non_important = True
            for val in m_tf_idf[dic_words[word]]:
                if val != 0.0:
                    non_important = False
            if non_important == False:
                result.append((word, m_tf_idf[dic_words[word]]))

    return result
"""

def tf_idf_question(dic_words, liste_of_files, question):
    """
    tf_idf_question : calcule le vecteur TF-IDF de la chaîne de caractère "question" donnée en entrée.
    - Entrées : dic_words = un dictionnaire des mots (key = mots, valeur = index (colonne) des mots dans la matrice"m_tf_idf") donnée par la fonction "tf_idf".
                liste_of_files = une liste de noms de fichiers (fichier du corpus étudier).
                question = une chaîne de caractères dont on veut le TF-IDF
    - Sortie : tf_idf_question = une matrice des vecteurs TF-IDF (colonne = fichier, ligne = mot) (elle possède le même paterne que la matrice tf_idf renvoyer par la fonction "tf_idf".
    /!\ si "question" est une chaîne de caractères vide alors la matrice "tf_idf_question" renvoyée sera composée de 0.0.
    """
    tok_question = tok(question)
    with open("question.txt", "w", encoding="utf-8") as file: # créer/modifie un fichier question qui permet de mêtre la variable "question" en fichier pour facilité le traitement notament pour le calcule de TF-IDF.
        file.write(" ".join(tok_question)) # créer le fichier a base de la toketisation de la variable "question".

    idf_corp = idf(liste_of_files, "cleaned")
    tf_idf_question = [0.0 for i in range(len(idf_corp))]
    tf_question = tf("question.txt", "")

    for word in tok_question:
        if word in idf_corp:
            tf_idf_question[dic_words[word]] = tf_question[word] * idf_corp[word]

    return tf_idf_question


### Calcul de la similarité ###


def transposed_matrix(matrix):
    """
    transposed_matrix : donne la transposée d'une matrice.
    - Entrées : matrix = une matrice.
    - Sortie : transposed_matrix = la transposée de la matrice "matrix".
    """
    if len(matrix) == 1 and len(matrix[0]) == 1: # si la matrice est de 1:1 alors sa transposer ne change rien a la matrice original (permet d'empécher des "out of range").
        return matrix

    transposed_matrix = [[None for k in range(len(matrix))] for i in range(len(matrix[0]))] # créer une matrice de len(matrix) colone et de len(matrix[0]) ligne (soit l'inverse de la matrice).

    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            transposed_matrix[i][j] = matrix[j][i]

    return transposed_matrix

def scalar_product(vector_a, vector_b):
    """
    scalar_product : donne le produit scalaire de deux vecteurs a et b.
    - Entrées : vector_a = un vecteur.
                vector_b = un vecteur.
    - Sortie : scalar_product = le produit scalaire du "vector_a" avec "vector_b".
    /!\ les deux vecteurs doivent être de longueur égale.
    """
    if len(vector_a) != len(vector_b):
        raise ValueError("Les deux vecteurs doivent être de longueurs différentes.") # erreur personnalisée si les deux vecteurs ne sont pas de longueurs égales.

    scalar_product = 0.0

    for k in range(len(vector_a)):
        scalar_product += vector_a[k] * vector_b[k]

    return scalar_product

def norm_vector(vector):
    """
    norm_vector : donne la norme d'un vecteur.
    - Entrées : vector = un vecteur.
    - Sortie : math.sqrt(norm_vector) = la norme du vecteur après l'application de la formule ||vector|| (trouvable sur le pdf de la partie II et III question 4.b.
    """
    norm_vector = 0.0

    for val in vector:
        norm_vector += val**2

    return math.sqrt(norm_vector)

def similarity(vector_a, vector_b):
    """
    similarity : calcule la similarité de deux vecteurs.
    - Entrées : vector_a = un vecteur.
                vector_b = un vecteur.
    - Sortie : (scalar_product(vector_a, vector_b)) / (norm_vector(vector_a) * norm_vector(vector_b)) = l'application de la formule de la similarité.
    /!\ les deux vecteur doivent être de longueur égale.
    """
    if len(vector_a) != len(vector_b):
        raise ValueError("Les deux vecteurs doivent être de longueurs différentes.") # erreur personnalisée si les deux vecteurs ne sont pas de longueur égale.

    return (scalar_product(vector_a, vector_b)) / (norm_vector(vector_a) * norm_vector(vector_b))

def best_sim_question(tf_idf_corp, tf_idf_question, dic_files):
    """
    best_sim_question : calcule du document le plus pertinent.
    - Entrées : tf_idf_corp = la matrice TF-IDF du corpus (de l'enssemble de la base de données).
                tf_idf_question = la matrice TF-IDF de la question/d'une phrase quelconque.
                dic_files = un dictionnaire des nom de fichier avec leur index (nécésaire pour la navigation dans les matrice TF-IDF)
    - Sortie : name_max_sim_question = le nom du fichier avec la plus grande similarité avec la matrice "tf_idf_question".
    """
    max_sim_question = 0.0
    name_max_sim_question = ""

    for name in dic_files:
        temp = similarity(transposed_matrix(tf_idf_corp)[dic_files[name]], tf_idf_question)
        if temp > max_sim_question:
            max_sim_question = temp
            name_max_sim_question = name

    return name_max_sim_question


### Génération d’une réponse ###


def sentences_in_file(file_name):
    """
    sentences_in_file : donne toutes les phrases d'un fichier.
    - Entrées : file_name = le nom d'un fichier du dossier "speeches".
    - Sortie : sentences = une liste de toutes les phrases du fichier "file_name".
    """
    sentences = []

    with open("speeches/"+file_name, "r", encoding="utf-8") as file:
        f_content = file.read()
        sentence = ""
        for carac in f_content:
            if carac == "." or carac == "\n":
                sentences.append(sentence)
                sentence = ""
            else:
                sentence += carac

    return sentences

def beautiful_awnser(str):
    """
    beautiful_awnser : print de façon plus ChatGPT-esque.
    - Entrées : str = une chaîne de caractères.
    - Sortie : des print de chaque caractère de la variable "str" a intervalles alléatoires (qui peut aller de 0.01s a 0.2s en fonction des caractères).
    """
    str += " "
    str_tab = str.split(" ")

    for word in str_tab:
        for char in word:
            if char in [".","!","?"]:
                print(char, end="")
                sleep(uniform(0.1, 0.5))
            elif char in [",", ";", ":"]:
                print(char, end="")
                sleep(uniform(0.05, 0.1))
            else:
                sleep(uniform(0.01, 0.05))
                print(char, end="")
        sleep(uniform(0.05, 0.2))
        print("", end=" ")

def awnser(tf_idf_corp, dic_files, dic_words, list_of_files, question):
    """
    awnser : donne une réponce a une question en se basant sur la base de données.
    - Entrées : tf_idf_corp = la matrice TF-IDF du corpus.
                dic_files = un dictionnaire des nom de fichiers avec leur index (nécessaire pour la navigation dans les matrice TF-IDF)
                dic_words = un dictionnaire des mots avec leur index (nécésaires pour la navigation dans les matrice TF-IDF)
                list_of_files = liste de tous les fichiers de la base de données
                question = la question
    - Sortie : sentence = la réponse a la question. C'est la première occurence du mot le plus important de la question dans le fichier avec la plus grande similarité avec la question.
    """
    tf_idf_quest = tf_idf_question(dic_words, list_of_files, question)

    interesting = False
    for val in tf_idf_quest:
        if val != 0.0: # si la matrice TF-IDF de la question n'est composé que de 0.0 alors la base de données ne peut pas répondre a la question (cas si aucun mot de la question n'est présent dans la base de données).
            interesting = True

    if interesting == True:
        best_sim = best_sim_question(tf_idf_corp, tf_idf_quest, dic_files)
        question_starters = {
            "Comment": "Après analyse, ",
            "Pourquoi": "Car, ",
            "Peux-tu": "Oui, bien sûr!"
        }
        max_tf_idf_quest = 0.0
        word_max_tf_idf_quest = ""

        for k in range(len(tf_idf_quest)):
            if tf_idf_quest[k] > max_tf_idf_quest:
                max_tf_idf_quest = tf_idf_quest[k]
                word_max_tf_idf_quest = list(dic_words.keys())[k]

        for sentence in sentences_in_file(best_sim):
            if word_max_tf_idf_quest in sentence:
                if question.split(" ")[0] in question_starters: # teste si le premier mot de la question peut recevoir un "starter".
                    return question_starters[question.split(" ")[0]] + sentence + "."
                else:
                    return sentence + "."

    return "La base de données ne peut pas répondre a cette question."
