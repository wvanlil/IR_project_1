bert_file = open("bert-base_msmarco-dev3.trec", "r")
write_file = open("anserini_ready_bert_run.tsv", "w")

for line in bert_file:
    line_split = line.split(" ")
    write_file.write(line_split[0] + "\t" + line_split[2] + "\t" + line_split[3] + "\n")
