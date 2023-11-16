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
