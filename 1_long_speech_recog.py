import sys
import os
import glob
import shutil
import subprocess
import speech_recognition as sr

# 音声ファイルの分割
import wave
import math
import struct
from scipy import fromstring, int16

# mp4から音声ファイルへの変換
def mp4_to_wav(mp4f):
  wavf = mp4f.replace('.mp4', '.wav')
  subprocess.run(['ffmpeg', '-i', mp4f, wavf], 
                  encoding='utf-8', stdout=subprocess.PIPE)
  return wavf

# 音声ファイルの分割(デフォルト30秒)
def cut_wav(wavf,time=30):
  # timeの単位は[sec]
  # ファイルを読み出し
  wr = wave.open(wavf, 'r')

  # waveファイルが持つ性質を取得
  ch = wr.getnchannels()
  width = wr.getsampwidth()
  fr = wr.getframerate()
  fn = wr.getnframes()
  total_time = 1.0 * fn / fr
  integer = math.floor(total_time) + 1  # 小数点以下切り捨て
  t = int(time)  # 秒数[sec]
  frames = int(ch * fr * t)
  num_cut = int(integer//t)

  # waveの実データを取得し、数値化
  data = wr.readframes(wr.getnframes())
  wr.close()
  X = fromstring(data, dtype=int16)
  
  # wavファイルを削除
  os.remove(wavf)
  
  outf_list = []
  for i in range(num_cut):
      # 出力データを生成
      output_dir = 'output/cut_wav/'
      os.makedirs(output_dir,exist_ok=True)
      outf = output_dir + str(i).zfill(3) + '.wav'
      start_cut = i*frames
      end_cut = i*frames + frames
      Y = X[start_cut:end_cut]
      outd = struct.pack("h" * len(Y), *Y)

      # 書き出し
      ww = wave.open(outf, 'w')
      ww.setnchannels(ch)
      ww.setsampwidth(width)
      ww.setframerate(fr)
      ww.writeframes(outd)
      ww.close()
      
      # リストに追加
      outf_list.append(outf)
  
  return outf_list

# 複数ファイルの音声のテキスト変換
def cut_wavs_str(outf_list):
  output_text = ''
  # 複数処理
  print('音声のテキスト変換')
  for fwav in outf_list:
      print(fwav)
      r = sr.Recognizer()
      
      # 音声->テキスト
      with sr.AudioFile(fwav) as source:
          audio = r.record(source)
      text = r.recognize_google(audio, language='ja-JP')
      
      # 各ファイルの出力結果の結合
      output_text = output_text + text + '\n'
      # wavファイルを削除
      #os.remove(fwav)
      
  return output_text


# mp4からwavへの変換から音声のテキスト変換まで
def mp4_to_text(mp4f):
  # 出力ディレクトリ
  shutil.rmtree('output/cut_wav/')
  os.makedirs('output/cut_wav/', exist_ok=True)
  
  # 音声ファイルへの変換
  wav_file = mp4_to_wav(mp4f)
  
  # 音声ファイルの分割(デフォルト30秒)
  cut_wavs = cut_wav(wav_file)
  
  # 複数ファイルの音声のテキスト変換
  out_text = cut_wavs_str(cut_wavs)
  
  # テキストファイルへの入力
  #mp4f_name = os.path.basename(mp4f)
  #txt_file = 'output/' + mp4f_name.replace('.mp4', '.txt')
  txt_file = 'output/ja.txt'
  print('テキスト出力')
  print(txt_file)
  f = open(txt_file, 'w')
  f.write(out_text)
  f.close()

# 変換の実行
mp4_to_text(sys.argv[1])
