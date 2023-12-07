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
"""

from fonction import *

if __name__ == '__main__':

    s_p_names = s_p_names("./speeches", ".txt")

    list_of_files = list_of_files("./speeches", ".txt")
    for file in list_of_files:
        clean_files(file)

    m_tf_idf, dic_files, dic_words = tf_idf(list_of_files)

    question = "je sUis tom pèRe monsieur, nous p"
    print(tok(question))
    print(question_in_corp(m_tf_idf, dic_files, dic_words, question))


    """
    ### affichage demander ###
    
    print("1. Mots les moins importants.")
    not_inportant = []
    for i_word in range(len(m_tf_idf)):
        result = True
        for i_file in range(len(m_tf_idf[0])):
            if m_tf_idf[i_word][i_file] != 0.0:
                result = False
            if i_file == len(m_tf_idf[0])-1 and result == True:
                not_inportant.append(list(dic_words.keys())[i_word])
    for word in not_inportant:
        print("    -", word)
    
    print(" ")
    print("2. Le mot avec le score TF-IDF le plus élevé.")
    word_max = ""
    max = 0
    words = dic_words.keys()
    for i_file in range(len(m_tf_idf[0])):
        for i_word in range(len(m_tf_idf)):
            if m_tf_idf[i_word][i_file] > max:
                max = i_word
                word_max = list(dic_words.keys())[i_word]
    print("    -", word_max)

    print(" ")
    print("3. Le mot le plus répété par Chirac")
    list_file_chirac = ["Nomination_Chirac1.txt", "Nomination_Chirac2.txt"]
    max_chirac = ""
    chirac_words = {}
    max = 0
    for file in list_file_chirac:
        chirac_words_temp = tf(file)
        for word in chirac_words_temp:
            if word in chirac_words:
                chirac_words[word] += chirac_words_temp[word]
            else:
                chirac_words[word] = chirac_words_temp[word]
    for word in chirac_words:
        if chirac_words[word] > max and word not in not_inportant:
            max = chirac_words[word]
            max_chirac = word
        elif chirac_words[word] == max and word not in not_inportant:
            max_chirac += word
    for word in max_chirac:
        print("    -", word)

    print(" ")
    print("4. les noms des présidents qui ont parlé de la « Nation » et celui qui l’a répété le plus de fois")
    p_nation_count = {
        "Giscard dEstaing": 0,
        "Chirac": 0,
        "Mitterrand": 0,
        "Macron": 0,
        "Sarkozy": 0,
        "Hollande": 0
    }
    def name_temp(name):
        name = name[11:(len(name)) - 4]
        while (ord(name[len(name) - 1]) >= 48) and (ord(name[len(name) - 1]) <= 57):
            name = name[:len(name) - 1]
        return name

    for file in list_of_files:
        nb_words = tf(file)
        for word in nb_words:
            if word == "nation" or word == "Nation":
                p_nation_count[name_temp(file)] += 1
    p_max = ""
    max = 0
    for p in p_nation_count:
        if p_nation_count[p] != 0:
            print("    -", p, "a dit nation.")

        if p_nation_count[p] > max:
            p_max = p
        elif p_nation_count[p] == max:
            p_max += " " + p
    print(" ")
    print("    -", p_max, "a dit le plus de fois nation.")

    print(" ")
    print("5. le premier président a avoir parler du climat.")
    for file in list_of_files:
        nb_words = tf(file)
        for word in nb_words:
            if word == "climat" or word == "écoàlogie":
                first = name_temp(file)
    print("    -", first)

    print(" ")
    print("6. les mot que tout les président on évoqués.")
    tab = []
    say1 = []
    say2 = []
    for file in list_of_files:
        tab.append(tf(file))
    for word in tab[0]:
        say1.append(word)
    for dic in tab:
        say2 = []
        for word in dic:
            if word in say1 :
                say2.append(word)
        say1 = say2
    for word in say1:
        print("    -", word)
    """