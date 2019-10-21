import os

output = "./data/total_google_play.csv"

files = os.listdir('./data/')
files = filter(lambda x: x.startswith("google_play"), files)

with open(output, "w", encoding="utf-8") as outf:
    for f in files:
        print(f"Read {f}")
        with open("./data/" + f, encoding='utf-8') as fin:
            lines = fin.readlines()
            outf.writelines(lines)