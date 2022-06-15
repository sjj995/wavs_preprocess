from xmlrpc.client import boolean
import librosa
import audio_metadata
from IPython.display import Audio
import soundfile as sf
import argparse
import sys
from pathlib import Path
import os
import json
from tqdm import tqdm
from tqdm import trange
import math

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default='/datadrive/vocoder/voxseg/mbc_radio_16k/wav.scp',
        help="config(wav.scp) path(Default: /datadrive/vocoder/voxseg/mbc_radio_16k/wav.scp)",
    )
    
    parser.add_argument(
        "-i",
        "--input_wav_path",
        type=str,
        default='/datadrive/vocoder/mbc_radio_22k_origin',
        help="Input wav file path(Default: stdin)",
    )
    
    parser.add_argument(
        "-vad",
        "--vad_info",
        type=str,
        default='/datadrive/vocoder/voxseg/mbc_radio_16k/segments',
        help="vad information path(Default: /datadrive/vocoder/voxseg/mbc_radio_16k/segments)",
    )

    parser.add_argument(
        "-o",
        "--output_wav_path",
        type=str,
        default='/datadrive/vocoder/vad_22k_dataset',
        help="output wav file path(Default: /datadrive/vocoder/vad_22k_dataset)",
    )

    
    return parser.parse_args()


def get_wav_list(config):
    wav_list = []
    with open(config,'r') as f:
        information = f.readlines()

    for info in information:
        wav_name = info.split(' ')[0]
        wav_file = wav_name+'_22k.wav'
        wav_list.append(wav_file)
    
    return wav_list


class TrimAudio:
    wav_piece = {}
    
    def __init__(self,sr,input_path,output_path,vad,*wavs):
        self.sr = sr
        self.input_path = input_path
        self.output_path = output_path
        self.vad = vad
        self.wav_list = wavs
        
    def get_duration(self,vad):
        with open(vad,'r',encoding='utf-8') as f:
            durations = f.readlines()
            for duration in durations:
                piece_name = duration.split(' ')[0]
                start_sec = duration.split(' ')[-2]
                end_sec = duration.split(' ')[-1].replace('\n','')
                TrimAudio.wav_piece[piece_name] = [start_sec,end_sec]
        return

    def trim_audio_data(self,sr,input_path,save_path):

        for k,v in tqdm(TrimAudio.wav_piece.items()):

            path = save_path+'/'+'_'.join(k.split('_')[:-2])
            if not os.path.exists(path):
                os.makedirs(path)
            
            wav_by_key = '_'.join(k.split('_')[:-2])+'_22k.wav'
            if wav_by_key in self.wav_list:
                audio_file = input_path+'/'+wav_by_key
                y, sr = librosa.load(audio_file, sr=sr)
                start_sec = float(v[0])-1 # 0초 이전이 포함될 경우 저장 X
                if start_sec < 0:
                    start_sec += 1
                end_sec = float(v[1])+1
        
                ny = y[math.floor(sr*start_sec):math.ceil(sr*end_sec)]
                if os.path.isfile(path+'/'+k+'.wav'): 
                    continue
                librosa.output.write_wav(path+'/'+k+'.wav', ny, sr)
            

    def exec_trimming(self):
        self.get_duration(self.vad)
        self.trim_audio_data(self.sr,self.input_path,self.output_path)


    
def main():
    args = get_args()

    if args.input_wav_path is None :
        f = sys.stdin
    else :
        assert os.path.exists(args.input_wav_path)
        wavs = get_wav_list(args.config)
        print(wavs)
        trim_audio = TrimAudio(22050,args.input_wav_path,args.output_wav_path,args.vad_info,*wavs) 
        trim_audio.exec_trimming()


    return
    

if __name__ == "__main__":

    main()
