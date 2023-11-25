import os

def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def p_names ():
    p_names = list_of_files("./speeches", ".txt")
    list_names = []
    for file in p_names :
        name = file[11 : len(file)-4]
        while ord(name[len(name)-1]) >= 48 and ord(name[len(name)-1]) <= 57 :
            name = name[:len(name)-1]
        if name not in list_names :
            list_names.append(name)
    return list_names


def clean_files(file_name):
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
