#!/usr/bin/env python3.11

""" Mitt svar på rabbel.se 
Helt plötsligt en dag var hela min familj rabbel-fantaster. Från tidig stund till sen kväll gick familjechatten varm.

Så, ja. Här är ett försök till ett program som hittar orden åt mig. """

# ordlistan från saol finns i en lista i filen words.py
from words import *

# A set is much faster than a list for reading. So let's convert it. 
word_set = set(word_list)

# fyll i bokstäverna från spelplanen i listan rabbel nedan

# 5 x 5 spelplan
rabbel = [
        ['k','l','l','n','f'],
        ['a','d','m','s','e'],
        ['r','v','b','s','p'],
        ['a','e','l','s','l'],
        ['n','s','e','o','r']
        ]

# 4 x 4 spelplan
""" rabbel = [
        ['o','r','i','l'],
        ['e','i','l','c'],
        ['n','r','m','d'],
        ['e','f','u','n']
        ] """


# Denna inaktiverade funktion checkar saol online efter ord. Har inte använt då den säkert blir väldigt seg. 
""" def check_word_exists(word):
    url = f"https://svenska.se/tri/f_saol.php?sok={word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if "SAOL gav inga svar" not in response.text:
        return True 
    else:
        return False """


# alla hittade ord sparas i denna lista
svar = []

# returnerar spelets inställningar
def set_vars():
    x_len = len(rabbel)
    y_len = len(rabbel[0])
    max_len = 9 #len(rabbel)*len(rabbel[0])
    return x_len,y_len,max_len

# här startar ordbyggnaden från varje bokstav på spelplan
def start(x_len,y_len,max_len):
    for x_index,row in enumerate(rabbel):
        for y_index,char in enumerate(row):
            word = []
            string = ''
            char = [x_index,y_index]
            char.append(rabbel[x_index][y_index])
            word.append(char)
            string += char[2]
            neighbours = get_neighbours(word,char,x_len,y_len)
            print('Starting with: ' + char[2])
            build(x_len,y_len,word,neighbours,max_len,string)
            word.pop()
            string = string[:-1]
            
    print(svar)  # skriver ut listan med ord då sökningen är klar

# bygger vidare på orden med upp till 8 ytterligare tecken och jämför alla kombinationer med ordlistan
def build(x_len,y_len,word,neighbours,max_len,string):
    for pos in neighbours:
        char = pos
        char.append(rabbel[pos[0]][pos[1]])
        word.append(char)
        string += char[2]
        neighbours2 = get_neighbours(word,char,x_len,y_len) # hittar angränsande bokstäver 
        if len(string) > 2:
            check_word(string)
        if len(string) > max_len:
            word.pop()
            string = string[:-1]
            break
        build(x_len,y_len,word,neighbours2,max_len,string) # gräver djupare
        word.pop()
        string = string[:-1]

# checkar varje bokstavssammansättning mot ordlistan från SAOL
def check_word(string):
    if string in word_set and string not in svar:
        print(string)
        svar.append(string)
        print(str(len(svar)) + ' ord')

# hittar angränsande kordinater i matrixen - utesluter de som redan är använda 
def get_neighbours(word,pos,x_len,y_len):
    neighbour_list = []
    for c in range(pos[0] -1, pos[0] + 2):
        for d in range(pos[1] - 1, pos[1] + 2):
            new_coordinate = [c,d]    
            if (new_coordinate != pos[0:2] and \
                0 <= new_coordinate[0] < x_len and \
                0 <= new_coordinate[1] < y_len and \
                new_coordinate not in [x[:2] for x in word]):
                neighbour_list.append(new_coordinate)
    return neighbour_list

def main():
    x_len,y_len,max_len = set_vars()
    start(x_len,y_len,max_len)

main()