import re
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

err = open('./Data/wiked.tok.err', 'r', encoding="utf-8")
cor = open('./Data/wiked.tok.cor', 'r', encoding="utf-8")

match_sentences = open('./Data/match_sentences.txt', 'w', encoding="utf-8")

vocab = set(line.strip() for line in open('./archive/vocab.tsv', 'r', encoding="utf-8"))


def checkVocab(sentence):
    split_sentence = word_tokenize(sentence.lower())
    if len(split_sentence) <= 5:
        return True

    for word in split_sentence:
        if word.strip() not in vocab:
            return True

    return False

def extractDif(good, wrong):
    good_split = word_tokenize(good.lower())
    wrong_split = word_tokenize(wrong.lower())

    index_left = 0
    for i in range(0, len(wrong_split)):
        if (i >= len(good_split) or wrong_split[i] != good_split[i]):
            index_left = i
            break

    index_right = 0
    for i in range(1, len(wrong_split)):
        if (wrong_split[len(wrong_split) - i] != good_split[len(good_split) - i]):
            index_right = len(wrong_split) - i + 1
            break

    sub_string = ""
    for i in range(0, len(wrong_split)):
        if i >= index_left - 2 and i <= index_right + 2:
            sub_string += wrong_split[i] + " "

    return sub_string

read_correct = []
read_wrong = []

c = 0

for line in err:
    read_wrong.append(line.strip())
    # c += 1
    # if c > 1000:
    #     break

c = 0

for line in cor:
    read_correct.append(line.strip())
    # c += 1
    # if c > 1000:
    #     break

patterns = []

for i in range(0, len(read_correct)):
    if read_correct[i] == read_wrong[i]:
        continue

    if checkVocab(read_correct[i]) or checkVocab(read_wrong[i]):
        continue

    anti_pattern = re.compile("[^a-z A-Z \d . , \- \t \n ’ : ?]")

    if anti_pattern.search(read_correct[i]) or anti_pattern.search(read_wrong[i]):
        continue

    # match_sentences.write(read_correct[i] + "\n")
    # match_sentences.write(read_wrong[i] + "\n")

    change = extractDif( "$ $ " + read_correct[i] + " $ $", "$ $ " + read_wrong[i] + " $ $")

    tagged = nltk.pos_tag(word_tokenize(change))

    tagged_sentence = ""
    for tag in tagged:
        tagged_sentence += str(tag[1]) + " "

    patterns.append(tagged_sentence)

    # match_sentences.write(tagged_sentence + "\n")
    # match_sentences.write(change + "\n\n")


match_sentences.write(str(Counter(patterns)))