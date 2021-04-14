import math
import random
def matthews(tp, tn, fp, fn):
    return (tp * tn - fp * fn) / math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))


def tune_threshold(threshold, seed, optimise):
    test_file = open('./archive/nyt/data_40k_new/test.tsv', 'r', encoding="utf-8")
    prediction_file = open('./archive/nyt/data_40k_new/experiment_lstm_pooling_classifier_h_1134_l_3_lr_0.0001_e_217_do_0.2.tsv', 'r', encoding="utf-8")

    test_vals = []
    for test_line in test_file:
        test_vals.append(int(test_line.split('\t')[1]))

    prediction_vals = []
    for prediction_line in prediction_file:
        prediction_vals.append(float(prediction_line))

    pair_vals = []
    for i in range(len(test_vals)):
        pair_vals.append((test_vals[i], prediction_vals[i]))
    
    random.Random(seed).shuffle(pair_vals)

    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0

    if optimise:
        start_index = 0
        total_len = int(len(test_vals) / 2)
    else:
        start_index = int(len(test_vals) / 2)
        total_len = len(test_vals)

    for i in range(start_index, total_len):
        if pair_vals[i][1] > threshold:
            if pair_vals[i][0] == 1:
                tp += 1
            else:
                fp += 1
        else:
            if pair_vals[i][0] == 1:
                fn += 1
            else:
                tn += 1
        total += 1

    accuracy = (tp + tn) / (total)

    return matthews(tp, tn, fp, fn), accuracy

max_mcc = 0
best_i = 0
errors = 0
for i in range(1000):
    try:
        new_mcc, new_acc = tune_threshold(i/1000, 1, True)
        if new_mcc > max_mcc:
            max_mcc = new_mcc
            best_i = i
    except:
        errors += 1
        
print("errors: " + str(errors))
print(max_mcc)
print(best_i/1000)

print(tune_threshold(best_i/1000, 1, False))