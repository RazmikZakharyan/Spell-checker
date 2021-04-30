import os
import json
import string as s


def distance(a: str, b: str) -> int:
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    array = [[i] for i in range(m + 1)]
    array[0] = list(range(n + 1))
    for i in range(1, m + 1):
        for j in range(n):
            if b[i - 1] != a[j]:
                array[i].append(min(array[i - 1][j] + 1, array[i - 1][j + 1] + 1, array[i][j] + 1))
            else:
                array[i].append(min(array[i - 1][j], array[i - 1][j + 1] + 1, array[i][j] + 1))
    return array.pop().pop()


def soundex(string: str) -> str:
    encoding_table = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 0,
        'F': 1,
        'G': 2,
        'H': 0,
        'I': 0,
        'J': 2,
        'K': 2,
        'L': 4,
        'M': 5,
        'N': 5,
        'O': 0,
        'P': 1,
        'Q': 2,
        'R': 6,
        'S': 2,
        'T': 3,
        'U': 0,
        'V': 1,
        'W': 0,
        'X': 2,
        'Y': 0,
        'Z': 2,
    }
    encode = ''.join([str(encoding_table[i.upper()]) for i in string[1:] if i != "\'"]).strip('0')
    encode_soundex = '000'
    count = 0
    flag = False
    for i in encode:
        if count == 3:
            break
        if i != '0':
            if encode_soundex[count - 1] != i or flag:
                encode_soundex = encode_soundex.replace('0', i, 1)
                count += 1
                flag = False
        else:
            flag = True

    return ''.join([string[0].upper(), encode_soundex])


def create_soundex_file():
    soundex_dict = {}
    with open(os.path.normpath('dictionary.txt'), 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            soundex_encrypt = soundex(line)
            if not soundex_dict.get(soundex_encrypt):
                soundex_dict.update({f'{soundex(line)}': [line]})
            else:
                soundex_dict.get(soundex_encrypt).append(line)
    json.dump(soundex_dict, open(os.path.normpath('soundexFile.text'), 'w'))


def is_valid(inputStr: str) -> bool:
    if not len(inputStr) > 31:
        for el in inputStr:
            if el not in s.ascii_letters:
                print(f'InputError: {el} is not a letter')
                break
        else:
            return True
    else:
        print('InputError: The input string is not a word')
    return False


if __name__ == '__main__':
    print("1. Levenshtein \n2. Soundex \n3. Spell correction")
    inputType = input("Type 1, 2 or 3: ").strip()

    if inputType == '1':
        firstString = input('First string: ')
        secondString = input('Second string: ')
        distance = distance(firstString, secondString)
        print(f'Levenshtein distance for "{firstString}" and "{secondString}" is {distance}')
    elif inputType == '2':
        inputString = input('Input string: ').strip()
        if is_valid(inputString):
            soundexCode = soundex(inputString)
            print(f'Soundex code for "{inputString}" is {soundexCode}')
    elif inputType == '3':
        word = input('Write misspelled word:')
        dictionary = eval(open(os.path.normpath('soundexFile.text'), 'r').read())
        if is_valid(word):
            optionsList = []
            soundexCode = soundex(word)
            options = dictionary.get(soundexCode)
            if options:
                for item in options:
                    distanceOptions = distance(word, item)
                    if 2 > distanceOptions:
                        optionsList.append(item)
                if optionsList:
                    print('Possible options: ', ', '.join(optionsList))
                else:
                    print('did not find possible options')
            else:
                print('did not find possible options')

    else:
        print(f'TypeError: Type 1, 2 or 3 not \'{inputType}\'')
