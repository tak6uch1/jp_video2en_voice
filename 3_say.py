import subprocess

with open('output/en.txt') as f:
    en_words = f.readlines()

cnt = 0
for src in en_words:
    ofile = 'output/en_voice/{:0=3}.wav'.format(cnt)
    print(ofile)
    cnt = cnt + 1
    subprocess.run(['say', '-o', ofile, '--data-format=LEF32@22050', src])


