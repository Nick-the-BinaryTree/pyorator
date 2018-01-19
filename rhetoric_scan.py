phrase_break = set(['.', ';', '!', '?'])
conjugation = set(['-', 'for', 'and', 'nor', 'but', 'or', 'yet'])

def getWord(s, i):
    word = ''
    while s[i] not in phrase_break and s[i] not in [' ', ',']:
        word += s[i]
        i+= 1
    return (word.lower(), i)

def rhetoric_scan(s):
    if s[-1] not in phrase_break: # add a period if there isn't a sentence ending
        s += '.'

    i = anaphora_count = epistrophe_count = anadiplosis_count = 0
    sen_last_starter, sen_start_row = com_last_starter, com_start_row = \
        sen_last_ender, sen_end_row = com_last_ender, com_end_row = None, 0
    new_sen, new_com = True, False
    word = before_conj = None

    while i < len(s):
        last_word = word
        word, i = getWord(s, i)
        if ((new_sen or new_com) and last_word == word) or (before_conj and before_conj == word):
            anadiplosis_count += 1
        before_conj = None
        if word in conjugation:
            before_conj = last_word
        if new_sen:
            new_sen = False
            if word != sen_last_starter:
                sen_last_starter, sen_start_row = com_last_starter, com_start_row = word, 1
            elif word:
                sen_start_row += 1
                if sen_start_row == 2:
                    anaphora_count += 1
        elif new_com:
            new_com = False
            if word != com_last_starter:
                com_last_starter, com_start_row = word, 1
            elif word:
                com_start_row += 1
                if com_start_row == 2:
                    anaphora_count += 1
        if s[i] in phrase_break:
            new_sen = True
            if word == com_last_ender:
                com_end_row += 1
                if com_end_row == 2:
                    epistrophe_count += 1
            com_last_ender, com_end_row = word, 0
            if word != sen_last_ender:
                sen_last_ender, sen_end_row = word, 1
            elif word:
                sen_end_row += 1
                if sen_end_row == 2:
                    epistrophe_count += 1
            i += 1
        elif s[i] == ',':
            new_com = True
            if word != com_last_ender:
                com_last_ender, com_end_row = word, 1
            elif word:
                com_end_row += 1
                if com_end_row == 2:
                    epistrophe_count += 1
            i += 1
        i += 1

    return "Anaphora count: " + str(anaphora_count) + " Epistrophe count: " + str(epistrophe_count) + " Anadiplosis count: " + str(anadiplosis_count)