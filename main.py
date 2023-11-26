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
