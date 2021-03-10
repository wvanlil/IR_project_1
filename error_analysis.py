import math
import string
import matplotlib.pyplot as plt


import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def plot_graph(inputs):

    x_coords = []
    for i in range(len(inputs)):
        x_coords.append([])

    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            x_coords[i].append((j / len(inputs[i]) * 100))
    
    max_len = 0
    for i in inputs:
        if len(i) > max_len:
            max_len = len(i)

    for i in range(len(inputs)):
        inputs[i].sort()
        line, = plt.plot(x_coords[i], inputs[i])
        if (i == 0):
            line.set_label("Not relevant")
        else:
            line.set_label("Relevant")

    plt.legend()
    plt.xlabel('Query elements')
    plt.ylabel('Word distance')
    plt.savefig('WordDistance.png')
    plt.show()


# Set this to True if reading from small collection file, otherwise it generates one
# Small collection file is only passages that are used in the run
read_from_small = True

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

sorted_by_qrels = [[],[]]

def precalc_passage(passage, passageId, file):
    passage_split = preprocess(passage)
    count = 0
    for word in passage_split:
        if word[1] == "NN" or word[1] == "NNP" or word[1] == "NNS":
            count+= 1

    if count > math.floor(len(passage_split) * 0.50):
        file.write(str(passageId) + '\n')

def calc_proximity(query, passage):
    query_split =  preprocess(query)

    want_to_remove = ['WDT', 'WP', 'DT', 'IN', 'PRP', 'PRP$', 'CC', 'EX']

    for i in range(len(query_split)):
        query_split[i] = (query_split[i][0].lower().translate(str.maketrans('', '', string.punctuation)), query_split[i][1])

    passage_split = preprocess(passage)
    for i in range(len(passage_split)):
        passage_split[i] = (passage_split[i][0].lower().translate(str.maketrans('', '', string.punctuation)), passage_split[i][1])
    
    ret = []

    occurrences = 0

    
    for i in range(len(query_split) - 1):
        if query_split[i][1] in want_to_remove:
            continue

        next_query_word = "&%$"
        for j in range(i, len(query_split)):
            if query_split[j][1] not in want_to_remove:
                next_query_word = query_split[j][0]
                break

        for j in range(len(passage_split)):
            if passage_split[j][0] in query_split[i]:
                for k in range(j + 1, len(passage_split)):
                    if passage_split[k][0] in next_query_word:
                        ret.append(k - j)
                        occurrences += 1
                        break
                    if  k - (j + 1) > 20:
                        break 
    
    actualret = 0
    
    for i in ret:
        actualret += i

    #actualret = actualret / (occurrences+1)

    return occurrences / (actualret + 1)

def frequent_occurrences(query, passage):
    occurrences = 0
    for q in query:
        for p in passage:
            if q in p:
                occurrences += 1
    return occurrences / (len(passage) * len(query))

# ----- Read queries into dict: {QueryID : Query string}

queries = open('./data/queries.tsv', 'r')

query_dict = {}

for queries_line in queries:
    q_split = queries_line.split('\t')
    query_dict[q_split[0]] = q_split[1]

queries.close()

# ----- Read qrels into dict: {(QueryID, PassageID) : Qrel Score}

qrels_dict = {}

qrels = open('./data/qrels.txt','r')

for qrels_line in qrels:
    q_split = qrels_line.split('\t')
    qrels_dict[(q_split[0], q_split[2])] = q_split[3]

qrels.close()

# ----- Read run by BM25 into array:

r_arr = []

run = open('./data/run.tsv', 'r')

i = 0
for run_line in run:
    if i < 30:
        r_split = run_line.split('\t')
        r_arr.append(r_split[1])
    elif i == 999:
        i = -1
    i += 1

run.close()

# ----- Fill the collection dict: {PassageID : Passage string}

collection_dict = {}

c = 0

if not read_from_small:
    collection = open('../anserini/collections/msmarco-passage/collection.tsv')
    for collection_line in collection:
        c += 1
        c_split = collection_line.split('\t')
        if c_split[0] in r_arr:
            print(c)
            collection_dict[c_split[0]] = c_split[1]
    collection.close()
    
    write_collection = open('./data/small_collection.txt', 'w')
    for item in collection_dict:
        write_collection.write(str(item) + '\t' + str(collection_dict[item]))
    write_collection.close()
    
else:
    collection = open('./data/small_collection.txt', 'r')
    for item in collection:
        i_split = item.split('\t')
        collection_dict[i_split[0]] = i_split[1]
    collection.close()

# ----- All data has been preprocessed, calc score from here

run2 = open('./data/run.tsv', 'r')

writefile = open('./data/output.txt', 'w')
skip_file = open('./data/skipfile.txt', 'w')
distance_file = open('./data/distancefile.txt', 'w')
distance_dict = {}
i = 0
for run_line in run2:
    if i < 30:
        r_split = run_line.split('\t')
        writefile.write(query_dict[r_split[0]])
        writefile.write(collection_dict[r_split[1]])
        
        qrel_val = 0
        if (r_split[0], r_split[1]) not in qrels_dict:
            writefile.write("Qrel score: " + str(-1) + '\n')
            qrel_val = -1
        else:
            writefile.write("Qrel score: " + qrels_dict[(r_split[0], r_split[1])])
            qrel_val = qrels_dict[(r_split[0], r_split[1])]

        writefile.write("Freq Occurrences: " + str(frequent_occurrences(r_split[0], r_split[1])))

        if i < 10:
            distance_dict[(r_split[0], r_split[1])] = calc_proximity(query_dict[r_split[0]], collection_dict[r_split[1]])
        
        calced_value = calc_proximity(query_dict[r_split[0]], collection_dict[r_split[1]])

        index = 1

        if int(qrel_val) < 1 :
            index = 0

        sorted_by_qrels[index].append(calced_value)
        #precalc_passage(collection_dict[r_split[1]], r_split[1], skip_file)
        
        #sorted_by_qrels[int(qrel_val)+1].append(query_val)
        #print("Query with score: " + str(query_val))
        
        writefile.write(str(calced_value) + '\n')
        writefile.write(r_split[2] + "\n")
    elif i == 999:
        print_dict = dict(sorted(distance_dict.items(), key=lambda item: item[1]))
        position = 1
        for key in print_dict.keys():
            distance_file.write(str(key[0] + '\t' + str(key[1]) + '\t' + str(position) + '\n'))
            position += 1
        distance_dict = {}
        i = -1
    i += 1

for i in range(len(sorted_by_qrels)):
    temp = 0
    for j in sorted_by_qrels[i]:
        temp += j
    #print(str(i-1) + " with avg: " + str(temp/len(sorted_by_qrels[i])))
    
plot_graph(sorted_by_qrels)