test_file = open('./archive/nyt/data_40k/test.tsv', 'r', encoding="utf-8").readlines()
prediction_file = open('./archive/nyt/data_40k/experiment_lstm_pooling_classifier_h_1134_l_3_lr_0.0001_e_217_do_0.2.tsv', 'r', encoding="utf-8").readlines()

# set threshold here
threshold = 0.7

# tag [correct, wrong]
data = {'nyt': [0, 0],
        'agr': [0, 0],
        'del': [0, 0],
        'spl': [0, 0],
        'swp': [0, 0],
        'shf': [0, 0],
        'xtr': [0, 0]}

for i in range(len(test_file)):
    if float(prediction_file[i]) > threshold:
        guess = 1
    else:
        guess = 0
    
    if guess == int(test_file[i].split('\t')[1]):
        data[test_file[i].split('\t')[0]][0] += 1
    else:
        data[test_file[i].split('\t')[0]][1] += 1

print(data)
