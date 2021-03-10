# IR_project_1

### Scripts
#### error_analysis.py
This script was used to analyse the BM25 run. It outputs the results with extra information such as qrel score and our own metrics. This script also generates the graphs.
#### msmarco_passage_eval.py
This script is supplied by anserini, but modifications have been made adjust for multiple-graded relevance levels.
#### run_converter.py
Filters the run to only use the top 30 of each query for our own improvements. Puts it in the right format as well.
#### convert_back.py
Converts the file from L2R trec format to tsv to be able to calculate the metrics using Anserini.
#### inference.py
This was part of OpenMatch, but was adjusted to work with our setup without cuda.
#### run_script
Command used to run L2R.
