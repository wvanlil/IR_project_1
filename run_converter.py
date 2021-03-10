run_file = open("run.tsv", 'r')
write_file = open('trec_run.trec', 'w')

it = 0

for line in run_file:
    it = (it + 1)%1000
    
    if (it > 0 and it <= 30):
        line_split = line.split('\t')
        write_str = ""
        write_str += line_split[0] + " Q0 "
        write_str += line_split[1] + " "
        write_str += line_split[2][:-1] + " "
        write_str += str(1/float(line_split[2])) + " anserini\n"
        write_file.write(write_str)
        
    
