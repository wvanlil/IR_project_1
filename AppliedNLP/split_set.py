import random

ratios = [0.9, 0.05, 0.05]

full_file = open('./archive/blogs/new_sentences_blogs.txt', 'r', encoding="utf-8")

train_set = open('./archive/blogs/data_40k_new/train.tsv', 'w', encoding="utf-8")
dev_set = open('./archive/blogs/data_40k_new/dev.tsv', 'w', encoding="utf-8")
test_set = open('./archive/blogs/data_40k_new/test.tsv', 'w', encoding="utf-8")

i = 0
for line in full_file:
    i += 1
    if i == 15000:
        break
    r = random.uniform(0, 1)
    if r < ratios[0]:
        train_set.write(line)
    elif r < ratios[0] + ratios[1]:
        dev_set.write(line)
    else:
        test_set.write(line)