import subprocess
from googletrans import Translator

translator = Translator()

with open('output/ja.txt') as f:
    jp_words = f.readlines()

en_words = []

for src in jp_words:
    dst = translator.translate(src, src='ja', dest='en')
    en_words.append(dst.text)
    print(dst.text)

with open('output/en.txt', 'w') as f:
    for src in en_words:
        f.writelines(src + "\n")

