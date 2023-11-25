### import ###

import os


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
        while (ord(name[len(name)-1]) >= 48) and (ord(name[len(name)-1]) <= 57):
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
