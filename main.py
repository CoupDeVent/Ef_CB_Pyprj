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
from affichage_demander import *

if __name__ == '__main__':

    s_p_names = s_p_names("./speeches", ".txt")

    list_of_files = list_of_files("./speeches", ".txt")
    for file in list_of_files:
        clean_files(file)

    m_tf_idf, dic_files, dic_words = tf_idf(list_of_files, "cleaned")

    #print(affichage_demander(m_tf_idf, dic_files, dic_words, list_of_files))

    question = "Comment une nation peut-elle prendre soin du climat ?"

    print(tf_idf_question(dic_words, list_of_files, question))