import sys
import os
import glob
import shutil
import subprocess
import speech_recognition as sr

import wave
import math
import struct
from scipy import fromstring, int16

# Convert mp4 to wav with ffmpeg
def mp4_to_wav(mp4f):
  wavf = mp4f.replace('.mp4', '.wav')
  subprocess.run(['ffmpeg', '-i', mp4f, wavf], 
                  encoding='utf-8', stdout=subprocess.PIPE)
  return wavf

# Split a voice file into 30 minute voice files
def cut_wav(wavf,time=30):
  wr = wave.open(wavf, 'r')

  # Read wav information
  ch = wr.getnchannels()
  width = wr.getsampwidth()
  fr = wr.getframerate()
  fn = wr.getnframes()
  total_time = 1.0 * fn / fr
  integer = math.floor(total_time) + 1
  t = int(time)  # sec]
  frames = int(ch * fr * t)
  num_cut = int(integer//t)

  # Read frames
  data = wr.readframes(wr.getnframes())
  wr.close()
  X = fromstring(data, dtype=int16)
  
  # Delete wav
  os.remove(wavf)
  
  outf_list = []
  for i in range(num_cut):
      # Generate output data
      output_dir = 'output/cut_wav/'
      os.makedirs(output_dir,exist_ok=True)
      outf = output_dir + str(i).zfill(3) + '.wav'
      start_cut = i*frames
      end_cut = i*frames + frames
      Y = X[start_cut:end_cut]
      outd = struct.pack("h" * len(Y), *Y)

      # Write to output file
      ww = wave.open(outf, 'w')
      ww.setnchannels(ch)
      ww.setsampwidth(width)
      ww.setframerate(fr)
      ww.writeframes(outd)
      ww.close()
      
      # Append to list
      outf_list.append(outf)
  
  return outf_list

# Convert multiple speech files to text files
def cut_wavs_str(outf_list):
  output_text = ''
  print('Convert speech to text')
  for fwav in outf_list:
      print(fwav)
      r = sr.Recognizer()
      
      # Convert
      with sr.AudioFile(fwav) as source:
          audio = r.record(source)
      text = r.recognize_google(audio, language='ja-JP')
      
      # Concat multiple text files
      output_text = output_text + text + '\n'
      # Delete wav
      #os.remove(fwav)
      
  return output_text

# Main routine
def mp4_to_text(mp4f):
  # Output directory
  shutil.rmtree('output/cut_wav/')
  os.makedirs('output/cut_wav/', exist_ok=True)
  
  # Convert video to voice
  wav_file = mp4_to_wav(mp4f)
  
  # Split voice file
  cut_wavs = cut_wav(wav_file)
  
  # Convert speech to text
  out_text = cut_wavs_str(cut_wavs)
  
  # Write text to a file
  #mp4f_name = os.path.basename(mp4f)
  #txt_file = 'output/' + mp4f_name.replace('.mp4', '.txt')
  txt_file = 'output/ja.txt'
  print('Output text')
  print(txt_file)
  f = open(txt_file, 'w')
  f.write(out_text)
  f.close()

# Execution
mp4_to_text(sys.argv[1])
