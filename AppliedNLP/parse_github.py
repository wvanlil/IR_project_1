import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

import re

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# github_file = open("./archive/github-typo/github-typo-corpus.v1.0.0.jsonl", 'r', encoding="utf-8")
github_file = open("./archive/github-typo/github_small.txt", 'r', encoding="utf-8")

write_file = open("./archive/github-typo/github-formatted.txt", 'w', encoding="utf-8")

vocab = set(line.strip() for line in open('./archive/vocab.tsv', 'r', encoding="utf-8"))

linecounter = 0

def isInVocab(sentence):
    words = word_tokenize(sentence)
    print(words)
    for i in range(len(words)):
        if words[i].strip() not in vocab:
            print("test")
            print(words[i].strip())
            return False

    return True

anti_pattern = re.compile("[^a-z A-Z \d . , \- \t \n ’ : ?]")

for line in github_file:
    if (linecounter == 0):
        line1 = line.lower()
    elif (linecounter == 1):
        line2 = line.lower()
    elif (linecounter == 2):
        if "true" in line:
            skip_flag = False
            sentences1 = sent_tokenize(line1)
            sentences2 = sent_tokenize(line2)
            if len(sentences1) != len(sentences2):
                continue

            full_sentences = sentences1 + sentences2
            for sent in full_sentences:
                if isInVocab(sent):
                    print("true")
                if not isInVocab(sent) or anti_pattern.search(sent):
                    skip_flag = True
                    break
            
            if skip_flag:
                continue

            for i in range(len(sentences1)):
                if sentences1[i] != sentences2[i]:
                    write_file.write(sentences1[i]+'\n')
                    write_file.write(sentences2[i]+'\n\n')

    else:
        linecounter = -1
            
    linecounter += 1