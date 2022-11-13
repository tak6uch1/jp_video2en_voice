# How to convert from Japanese video to voice files in English

This environment is for generating English voices from a video in Japanese.

If your machine is mac, the following 3 programs can work.

But for windows and linux, the 3_say.py does not work.

## Preparation on miniconda
    conda install scipy

## Execution method
    python 1_long_speech_recog.py
    python 2_translate.py
    python 3_say.py

## Function of scripts
- 1_long_speech_recog.py: Cut video into 30 seconds' short videos and make Japanese texts using SpeechRecognition library. 
- 2_translate.py: Translate Japanese texts into English using GoogleTrans.
- 3_say.py: Make English voice files from English tests using say command of Mac.

## Intermediate files and the output
- output/ja.txt: Japanese text file
- output/en.txt: English text file
- output/en_voice/*.wav: Output voice files in English (Mac only)
