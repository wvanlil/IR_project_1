import re
import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from difflib import get_close_matches

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def main():
    # articles = open('./archive/nytimes_news_articles.txt', 'r', encoding="utf-8")
    articles = open('./archive/blogs/blogger_text_only.txt', 'r', encoding="utf-8")

    vocab = set(line.strip() for line in open('./archive/vocab.tsv', 'r', encoding="utf-8"))

    # split_sentences = open('./archive/split_sentences.txt', 'w', encoding="utf-8")
    split_sentences = open('./archive/blogs/split_sentences.txt', 'w', encoding="utf-8")

    # pos_tags = open('./archive/postag.txt', 'w', encoding="utf-8")

    skiplines = 3

    for line in articles:
        if skiplines > 0:
            skiplines -= 1
            continue

        if len(line) == 0:
            skiplines = 3
            continue

        sentences = sent_tokenize(line)

        # pattern = re.compile("^[A-Za-z0-9.,;:’]*$")
        anti_pattern = re.compile("[^a-z A-Z \d . , \- \t \n ’ : ?]")

        for single_sentence in sentences:
            if anti_pattern.search(single_sentence):
                continue

            single_sentence = re.sub(r'[0-9]*[.][0-9]+', '0.1', single_sentence)
            single_sentence = re.sub(r'(?:\d\d\d*|[2-9])', '2', single_sentence)
            single_sentence = re.sub(r'’', '\'', single_sentence).lower()

            pre_sentence = ""
            full_sentence = ""

            tokenized_sentence = word_tokenize(single_sentence)

            if len(tokenized_sentence) < 5:
                continue

            makeErrors = True
            chance = 0.1

            correct_sentence = tokenized_to_sentence(tokenized_sentence, vocab, False)
            if correct_sentence is None:
                continue

            split_sentences.write(correct_sentence + "\n")

            if makeErrors:
                new_sentence = None

                r = random.uniform(0, 1)
                if r < chance:
                    new_sentence = agreement(tokenized_sentence, vocab)
                    if new_sentence is not None:
                        new_sentence = "agr\t0\t*\t" + new_sentence
                elif r < chance * 2:
                    new_sentence = word_delete(tokenized_sentence, vocab)
                    if new_sentence is not None:
                        new_sentence = "del\t0\t*\t" + new_sentence
                elif r < chance * 3:
                    new_sentence = spelling(tokenized_sentence, vocab)
                    if new_sentence is not None:
                        new_sentence = "spl\t0\t*\t" + new_sentence
                elif r < chance * 4:
                    new_sentence = sentence_to_wordswap(tokenized_sentence, vocab)
                    if new_sentence is not None:
                        new_sentence = "swp\t0\t*\t" + new_sentence
                elif r < chance * 5:
                    new_sentence = sentence_to_wordshift(tokenized_sentence, vocab)
                    if new_sentence is not None:
                        new_sentence = "shf\t0\t*\t" + new_sentence
                elif r < chance * 6:
                    new_sentence = extra_word(tokenized_sentence, vocab)
                    if new_sentence is not None:
                        new_sentence = "xtr\t0\t*\t" + new_sentence

                if r < chance * 6:
                    if new_sentence == None:
                        #print(r)
                        #print(tokenized_sentence)
                        continue
                    else:
                        split_sentences.write(new_sentence + "\n")


def tokenized_to_sentence(tokenized_sentence, vocab, error=False):
    if (not error):
        pre_sentence = "nyt\t1\t\t"
    else:
        pre_sentence = ""

    full_sentence = pre_sentence

    for i in range(len(tokenized_sentence)):
        if tokenized_sentence[i].strip() not in vocab:
            return None
        full_sentence += tokenized_sentence[i] + " "

    full_sentence = full_sentence[:-1]
    return full_sentence


def sentence_to_wordswap(tokenized_sentence, vocab):
    tagged = nltk.pos_tag(tokenized_sentence)
    max_while_iterations = 20
    while True:
        changeFrom = random.randrange(len(tokenized_sentence) - 1)
        changeTo = random.randrange(len(tokenized_sentence) - 1)

        if tagged[changeFrom][1] == tagged[changeTo][1]:
            continue

        if changeFrom != changeTo:
            break

        max_while_iterations -= 1
        if max_while_iterations == 0:  # hasn't found a possibility
            return None

    temp = tokenized_sentence[changeFrom]
    tokenized_sentence[changeFrom] = tokenized_sentence[changeTo]
    tokenized_sentence[changeTo] = temp

    return tokenized_to_sentence(tokenized_sentence, vocab, True)


def sentence_to_wordshift(tokenized_sentence, vocab):
    max_while_iterations = 20
    tagged = nltk.pos_tag(tokenized_sentence)
    adjectives = ["JJ", "JJR", "JJS"]
    while True:
        changeFrom = random.randrange(len(tokenized_sentence) - 1)
        changeTo = random.randrange(len(tokenized_sentence) - 1)

        if tagged[changeFrom][1] in adjectives:
            continue

        if changeFrom != changeTo:
            break

        max_while_iterations -= 1
        if max_while_iterations == 0:  # hasn't found a possibility
            return None

    shifted_word = tokenized_sentence.pop(changeFrom)
    tokenized_sentence.insert(changeTo, shifted_word)

    return tokenized_to_sentence(tokenized_sentence, vocab, True)

def word_delete(tokenized_sentence, vocab):
    tagged = nltk.pos_tag(tokenized_sentence)
    remove = ["DT", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "IN", "PRP", "PRP$", "NN", "NNS", "TO", "CC"]
    chance = [0.28, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.21, 0.05, 0.05, 0.035, 0.035, 0.07, 0.03]

    max_while_iterations = 20
    while True:

        random_remove = random.choices(remove, chance)
        random_index = random.randrange(0, len(tokenized_sentence))

        for i in range(len(tokenized_sentence)):
            if tagged[(i + random_index) % len(tokenized_sentence)][1] == random_remove[0]:
                tokenized_sentence.pop((i + random_index) % len(tokenized_sentence))
                return tokenized_to_sentence(tokenized_sentence, vocab, True)

        max_while_iterations -= 1
        if max_while_iterations == 0:  # hasn't found a possibility
            return None

def spelling(tokenized_sentence, vocab):
    max_while_iterations = 20
    while True:

        random_index = random.randrange(0, len(tokenized_sentence))
        matches = get_close_matches(tokenized_sentence[random_index], vocab)

        if len(matches) > 1:
            tokenized_sentence[random_index] = matches[1]
            return tokenized_to_sentence(tokenized_sentence, vocab, True)

        max_while_iterations -= 1
        if max_while_iterations == 0:  # hasn't found a possibility
            return None

def extra_word(tokenized_sentence, vocab):
    tagged = nltk.pos_tag(tokenized_sentence)
    max_while_iterations = 20

    while True:
        random_index = random.randrange(0, len(tokenized_sentence))
        adjectives = ["JJ", "JJR", "JJS"]

        for i in range(len(tokenized_sentence)):
            index = (i + random_index) % len(tokenized_sentence)
            if tagged[index][1] not in adjectives:
                tokenized_sentence.insert(index, tagged[index][0])
                return tokenized_to_sentence(tokenized_sentence, vocab, True)

        max_while_iterations -= 1
        if max_while_iterations == 0:  # hasn't found a possibility
            return None

def agreement(tokenized_sentence, vocab):
    original =["were" , "make", "saying", "walking", "ran", "man", "woman", "become", "a" , "these", "has" , "to" , "are" , "am"  , "had", "is" , "better", "worse", "more", "as much"   , "bigger" , "than", "as" , "easy"]
    replace = ["where", "made", "say"   , "walk"   , "run", "men", "women", "became", "an", "this" , "have", "too", "have", "be"  , "was", "are", "best"  , "worst", "most", "as much as", "biggest", "that", "than", "easiest"]
    max_while_iterations = 20

    while True:
        random_list = random.randrange(0, 2)
        random_index = random.randrange(0, len(tokenized_sentence))

        if random_list == 0:
            if tokenized_sentence[random_index] in original:
                tokenized_sentence[random_index] = replace[original.index(tokenized_sentence[random_index])]
                return tokenized_to_sentence(tokenized_sentence, vocab, True)
        else:
            if tokenized_sentence[random_index] in replace:
                tokenized_sentence[random_index] = original[replace.index(tokenized_sentence[random_index])]
                return tokenized_to_sentence(tokenized_sentence, vocab, True)

        max_while_iterations -= 1
        if max_while_iterations == 0:  # hasn't found a possibility
            return None


if __name__ == "__main__":
    main()