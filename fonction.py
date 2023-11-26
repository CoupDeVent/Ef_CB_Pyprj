### import ###


import os
import math


### Fonctions de base ###

def list_of_files(directory, extension):
    """
    list_of_files : liste tous les noms de fichier dans un dossier.
    - Entrées : directory = dossier des fichiers a listés. // extension = l'extension commune de tous les fichiers.
    - Sortie : files_names = une liste de tous les noms des fichiers listés.
    """
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def s_p_names(directory, extension):
    """
        s_p_names : donne tous les noms des présidents grâce à un dossier spécifié en entrée en suivant la logique de nomination des fichiers speeches.
        - Entrées : directory = dossier des fichiers. // extension = l'extension commune de tous les fichiers.
        - Sortie : p_names = une liste de tous les prénoms et nom des présidents du dossier.
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
        clean_files : clean le fichier donné en entrée de toutes ses : majuscules, marques de ponctuation, espaces supérieurs à 1 et sauts de ligne. (fichier ouvert en utf-8)
        - Entrées : file_name = nom du fichier a clean.
        - Sortie : créer/modifie un fichier du même nom dans un dossier "cleaned" avec les modifications.
        /!\ : nécessite un dossier "cleaned" créé au préalable.
        /!\ : si fichier déjà présent dans le dossier "cleaned" alors son contenu sera écrasé.
    """
    with open("speeches/"+file_name, "r", encoding="utf-8") as file, open("cleaned/"+file_name, "w", encoding="utf-8") as file_clean:
        f_content = file.read()
        new_content = ""
        world = ""
        for carac in f_content:
            if (ord(carac) >= 65 and ord(carac) <= 90) or (ord(carac) >= 192 and ord(carac) <= 223):
                world += chr(ord(carac)+32)
            elif (ord(carac) >= 97 and ord(carac) <= 122) or (ord(carac) >= 224 and ord(carac) <= 255):
                world += carac
            elif world != "":
                new_content += world + " "
                world = ""
        file_clean.write(new_content)


### TF-IDF ###


def tf(file_name):
    """
        tf : Donne la fréquence d'un terme dans un fichier.
        - Entrées : file_name = nom du fichier a tf-idéiser.
        - Sortie : dic_of_words = un dictionnaire de tous les mots du fichier avec leur fréquence.
    """
    with open("cleaned/"+file_name, "r", encoding="utf-8") as file:
        f_content = file.read()
        dic_of_words = {}
        word = ""
        for carac in f_content:
            if carac != " ":
                word += carac
            else:
                if word in dic_of_words:
                    dic_of_words[word] += 1
                    word = ""
                else:
                    dic_of_words[word] = 1
                    word = ""
        return dic_of_words

def idf(list_of_files):
    """
        idf : Calcule le score IDF (log((nb_fichier/nb_fichier_mot) + 1)) de chaque mot dans un dictionnaire.
        - Entrées : list_of_files = liste de nom de fichier.
        - Sortie : idf_dic = un dictionnaire de tous les scores IDF de tous les mots de tous les fichiers de la liste de nom de fichier donnés en entrée.
    """
    words_of_files = {}
    for file in list_of_files:
        dic = tf(file)
        for key in dic:
            if key in words_of_files:
                words_of_files[key] += 1
            else:
                words_of_files[key] = 1
    idf_dic = {}
    for key in words_of_files:
        idf_dic[key] = math.log((len(list_of_files)/words_of_files[key])) # calcule du score idf : log((nb_fichier/mot) + 1)
    return idf_dic

def tf_idf(list_of_files):
    """
        tf_idf : Calcule le score TF-IDF grace au deux dictionnaire donné par les deux fonctions ("tf" et "idf").
        - Entrées : list_of_files = liste de nom de fichier.
        - Sortie : m_tf_idf = une matrice des vecteur TF-IDF (colonne = fichier, ligne = mot)
                   dic_files = un dictionnaire des fichier (key = nom du fichier, valeur = index (colonne) des fichiers dans la matrice "m_tf_idf")
                   dic_words = un dictionnaire des mots (key = mots, valeur = index (colonne) des mots dans la matrice"m_tf_idf")
        /!\ la sortie des 3 variable se fait en tuple.
    """
    idf_dic = idf(list_of_files)
    m_tf_idf = [[0 for k in range(len(list_of_files))] for i in range(len(idf_dic))] # création d'un tableau de "len(list_of_files)" lignes et de "len(idf_dic)" colonnes.
    dic_files = {file: k for file, k in zip(list_of_files, range(len(list_of_files)))} # création d'un dictionnaire de key = "file" dans "list_of_files" et valeur = "k" = compteur de longueur de "list_of_file".
    dic_words = {word: k for word, k in zip(idf_dic, range(len(idf_dic)))} # création d'un dictionnaire de key = "word" dans "idf_dic" et valeur = "k" = compteur de longueur de "idf_dic".

    for file in list_of_files:
        tf_dic = tf(file)
        for word in tf_dic:
            m_tf_idf[dic_words[word]][dic_files[file]] = tf_dic[word] * idf_dic[word] # calcule vecteur TF-IDF a l'emplacement du mot dans la matrice (ligne = valeur du mot dans le dictionnaire "dic_words", colonne = valeur du nom du fichier dans le dictionnaire "dic_files").

    return (m_tf_idf, dic_files, dic_words) # tuple








