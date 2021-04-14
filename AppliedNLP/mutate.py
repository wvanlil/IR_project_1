import nltk
import random
import math
from nltk.tokenize import word_tokenize

new_sentences = open('./Data/new_sentences_blogs.txt', 'w', encoding="utf-8")
sentences = open('./Archive/split_sentences_blogs.txt', 'r', encoding="utf-8")
vocab = set(line.strip() for line in open('./archive/vocab.tsv', 'r', encoding="utf-8"))
patterns = open('./archive/patterns.txt', 'r', encoding="utf-8")

pattern_list = []

for pat in patterns:
    pattern_list.append(pat)

voc_dict = {}

for word in vocab:
    tagged = nltk.pos_tag(word_tokenize(word))[0]

    if tagged[1] in voc_dict:
        temp = voc_dict[tagged[1]]
        temp.append(tagged[0])
        voc_dict[tagged[1]] = temp
    else:
        voc_dict[tagged[1]] = [tagged[0]]

lines = []

def errorLine(tagged, partTarget, insert, front):

    nline = ""

    index = -100
    if front:
        r = range(len(tagged) - 1, 0, -1)
        indexTarget = len(partTarget) - 1
    else:
        r = range(0, len(tagged))
        indexTarget = 0

    for i in r:
        # print(str(front) + str(i) + " / " + str(indexTarget) + " / " + str(len(partTarget)))
        if tagged[i][1] == partTarget[indexTarget]:
            if front:
                index = i - 1
                indexTarget -= 1
                if indexTarget == 0:
                    break
            else:
                index = i
                indexTarget += 1
                if indexTarget == len(partTarget):
                    break
        else:
            if front:
                if tagged[i][1] == partTarget[len(partTarget) - 1]:
                    indexTarget = len(partTarget) - 2
                else:
                    indexTarget = len(partTarget) - 1
            else:
                if tagged[i][1] == partTarget[0]:
                    indexTarget = 1
                else:
                    indexTarget = 0

            index = -100

    if index < 0:
        return None

    for ins in insert:

        if ins not in voc_dict:
            print("Not found key")
            return None

        tag = random.choice(voc_dict[ins])
        tagged.insert(index, [tag, ins])
        index += 1

    for i in range(2, len(tagged)-2):
        nline += str(tagged[i][0]) + " "

    return nline + "\n"

for line in sentences:
    nline = line.split("\t")[3]
    lines.append("$ $ " + nline + " $ $")

for line in lines:
    tagged = nltk.pos_tag(word_tokenize(line))
    tagged_str = ""
    for tag in tagged:
        tagged_str += str(tag[1]) + " "

    for i in range(0, 20):
        target = random.choice(pattern_list).split()
        front = False
        if target[-1] == "$" or target[-1] == ".":
            ind = random.randrange(1, len(target)-2)
            partTarget = target[ind:]
            insert = target[0:ind]
            front = True
        else:
            ind = random.randrange(1, len(target)-2)
            partTarget = target[:-ind]
            insert = target[-ind:]

        partTarget_str = ""
        for targ in partTarget:
            partTarget_str += str(targ) + " "

        if partTarget_str in tagged_str:
            new_sentences.write("nyt\t1\t\t" + line[4:-4])

            error = errorLine(tagged, partTarget, insert, front)

            if error == None:
                print("error")
                continue

            new_sentences.write("nyt\t0\t*\t" + error)

            # new_sentences.write("Target: " + str(target) + "\n")
            break
