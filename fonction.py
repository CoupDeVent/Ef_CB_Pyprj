### import ###


import os
import math


### Fonctions de base ###

def list_of_files(directory, extension):
    """
    list_of_files : liste tout les noms de fichier dans un dossier.
    - Entrées : directory = dossier des fichiers a listés. // extension = l'extension commune de tout les fichiers.
    - Sortie : files_names = une liste de tout les noms des fichiers listés.
    """
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def s_p_names(directory, extension):
    """
        s_p_names : donne tout les noms des présidents grace a un dossier spécifier en entré en suivant la logique de nomination des fichiers speeches.
        - Entrées : directory = dossier des fichiers. // extension = l'extension commune de tout les fichiers.
        - Sortie : p_names = une liste de tout les prénom et nom des président du dossier.
        /!\ : tout les fichiers du dossier doivent suivre une nomination spécifique.
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
        clean_files : clean le fichier donné en entré de toutes ses : majuscule, marque de ponctuation, espace supérieur a 1 et saut de ligne. (fichier ouvert en utf-8)
        - Entrées : file_name = nom du fichier a clean.
        - Sortie : créer/modifie un fichier du même nom dans un dossier "cleaned" avec les modification.
        /!\ : nécésite un dossier "cleaned" créer au préalable.
        /!\ : si fichier déjà présent dans le dossier "cleaned" alors son contenu sera écraser.
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
        - Sortie : dic_of_words = un dictionnaire de tout les mots du fichier avec leur fréquence.
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
        idf : Calcule le score IDF (log((nb_fichier/mot) + 1)) de chaque mot dans un dictionnaire.
        - Entrées : list_of_files = liste de nom de fichier.
        - Sortie : idf_dic = un dictionnaire de tout les score IDF de tout les mot de tout les fichier de la liste de nom de fichier donné en entré.
    """
    words_of_files = {}
    for file in list_of_files:
        dic = tf(file)
        for key in dic:
            if key in words_of_files:
                words_of_files[key] += dic[key]
            else:
                words_of_files[key] = dic[key]
    idf_dic = {}
    for key in words_of_files:
        idf_dic[key] = math.log((len(list_of_files)/words_of_files[key]) + 1) # calcule du score idf : log((nb_fichier/mot) + 1)
    return idf_dic

def tf_idf(list_of_files):
    """
        tf_idf : Calcule le score TF-IDF grace au deux dictionnaire donné par les deux fonctions ("tf" et "idf").
        - Entrées : list_of_files = liste de nom de fichier.
        - Sortie : m_tf_idf = une matrice des vecteur TF-IDF (colonne = fichier, ligne = mot)
                   dic_column = un dictionnaire des fichier (key = nom du fichier, valeur = index (colonne) des fichiers dans la matrice "m_tf_idf")
                   dic_line = un dictionnaire des mots (key = mots, valeur = index (colonne) des mots dans la matrice"m_tf_idf")
        /!\ la sortie des 3 variable se fait en tuple.
    """
    idf_dic = idf(list_of_files)
    m_tf_idf = [[[] for k in range(len(list_of_files))] for i in range(len(idf_dic))] # création d'un tableau de "len(list_of_files)" lignes et de "len(idf_dic)" colonnes.
    dic_column = {file: k for file, k in zip(list_of_files, range(len(list_of_files)))} # création d'un dictionnaire de key = "file" dans "list_of_files" et valeur = "k" = compteur de longueur de "list_of_file". (zip() permet de mettre les deux variable en tuple pour les utiliser dans comme valeurs de boucle.) 
    dic_line = {word: k for word, k in zip(idf_dic, range(len(idf_dic)))} # création d'un dictionnaire de key = "word" dans "idf_dic" et valeur = "k" = compteur de longueur de "idf_dic".

    for file in list_of_files:
        tf_dic = tf(file)
        for word in tf_dic:
            m_tf_idf[dic_line[word]][dic_column[file]] = tf_dic[word] * idf_dic[word] # calcule vecteur TF-IDF a l'emplacement du mot dans la matrice (ligne = valeur du mot dans le dictionnaire "dic_ligne", colonne = valeur du nom du fichier dans le dictionnaire "dic_column").

    return (m_tf_idf, dic_column, dic_line) # tuple






