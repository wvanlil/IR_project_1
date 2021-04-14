import re
import os

write_file = open("./archive/blogs/blogger_text_only.txt", 'w', encoding="utf-8")

written_single = True

for subdir, dirs, files in os.walk("./archive/blogs/blogs"):
    for single_file in files:
        try:
            current_file = open(os.path.join(subdir, single_file), 'r', encoding="utf-8")
            written_single = True
            for line in current_file:
                if line[0] == '<':
                    continue
                if line.strip() == "":
                    continue
                if written_single == True:
                    write_file.write(single_file + "\n\n")
                    written_single = False
                write_file.write(line.lstrip())
            write_file.write("\n")
        except:
            print("exception")
            if written_single == False:
                write_file.write("\n")
