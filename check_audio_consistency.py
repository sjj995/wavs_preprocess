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

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input_wav_path",
        type=str,
        help="Input text file path(Default: stdin)",
    )

    parser.add_argument(
        "-sr",
        "--sample_rate",
        type=int,
        default=22050,
        help="resample rate(Default: 22050)",
    )

    parser.add_argument(
        "-c",
        "--channels",
        type=int,
        default=1,
        help="change channels(Default: 1)",
    )
    

    parser.add_argument(
        "-min_d",
        "--min_duration",
        type=int,
        default=1,
        help="min duration value(Default: 1)",
    )

    parser.add_argument(
        "-max_d",
        "--max_duration",
        type=int,
        default=100,
        help="max duration value(Default: 100)",
    )

    parser.add_argument(
        "-r",
        "--remove_failed_wav",
        type=boolean,
        default=False,
        help="remove unsatisfied duration files(Default: false)",
    )

    parser.add_argument(
        "-m",
        "--merge_wav_file",
        type=boolean,
        default=False,
        help="merge wav file in one directory(Default: false)",
    )

    parser.add_argument(
        "-csr",
        "--convert_sample_rate",
        type=boolean,
        default=False,
        help="convert sample rate(Default: false)",
    )

    parser.add_argument(
        "-cc",
        "--convert_channels",
        type=boolean,
        default=False,
        help="convert channel to mono(Default: false)",
    )

    parser.add_argument(
        "-cp",
        "--config_path",
        type=str,
        default=os.getcwd()+'/invalid_data',
        help="invalid information path(Default: os.getcwd()+'/invalid_data')",
    )



    return parser.parse_args()


def get_wav_files(root_path):
    wav_list = []
    for (root, dirs, files) in os.walk(root_path):
        for file_name in files:
           if file_name.endswith(".wav"):
                file_path = os.path.join(root,file_name)
                wav_list.append(file_path)
    
    return wav_list

class CheckAudio:
    invalid_info = ['invalid_rate','invalid_channels','invalid_duration']
    invalid_rate = {}
    invalid_channels = {}
    invalid_duration = {}

    def __init__(self,sr,channels,min_d,max_d,convert_sr_flag,convert_c_flag,remove_flag,config_file,*wavs):
        self.sr = sr
        self.channels = channels
        self.min_d = min_d
        self.max_d = max_d
        self.wav_list = wavs
        self.sr_flag = convert_sr_flag
        self.c_flag = convert_c_flag
        self.remove_flag = remove_flag
        self.config_file = config_file

    def audio_info(self,wav):
        metadata = audio_metadata.load(wav)
        return metadata
    

    def check_sample_rate(self,sampling_rate,metadata):
        if sampling_rate != metadata['streaminfo']['sample_rate']:
            CheckAudio.invalid_rate[metadata['filepath']] = metadata['streaminfo']['sample_rate']
            #print(f"sample rate is not correct at {sampling_rate}\n file : {metadata['filepath']}")
        return

    def check_channel(self,channels,metadata):
        if channels != metadata['streaminfo']['channels']:
            CheckAudio.invalid_channels[metadata['filepath']] = metadata['streaminfo']['channels']
            #print(f"channel is not correct at {channels}\n file : {metadata['filepath']}")    
        return

    def check_duration(self,min_d,max_d,metadata):
        if metadata['streaminfo']['duration'] < min_d:
            CheckAudio.invalid_duration[metadata['filepath']] = metadata['streaminfo']['duration']
            #print(f"duration is too short!!\n file : {metadata['filepath']}")
        elif metadata['streaminfo']['duration'] >= max_d+1:  
            CheckAudio.invalid_duration[metadata['filepath']] = metadata['streaminfo']['duration']
            #print(f"duration is too long!!\n file : {metadata['filepath']}")
        else:
            pass
            #print("duration check complete")
        return

    def write_result(self,path):
        if not os.path.exists(path):
            os.makedirs(path)
        
        if len(CheckAudio.invalid_rate) != 0:
            #output = path+'/'+'invalid_rate'+'.txt'
            output = path+'/'+'invalid_rate'+'.json'
            json.dump(CheckAudio.invalid_rate,open(output,'w',encoding='utf-8'))

        if len(CheckAudio.invalid_channels) != 0:
            #output = path+'/'+'invalid_channels'+'.txt'
            output = path+'/'+'invalid_channels'+'.json'
            json.dump(CheckAudio.invalid_channels,open(output,'w',encoding='utf-8'))    

        if len(CheckAudio.invalid_duration) != 0:
            #output = path+'/'+'invalid_duration'+'.txt'
            output = path+'/'+'invalid_duration'+'.json'   
            json.dump(CheckAudio.invalid_duration,open(output,'w',encoding='utf-8'))
        
        return

    def resampling_rate(self,resample_sr,metadata):
        input_wav = metadata['filepath']
        origin_sr = metadata['streaminfo']['sample_rate']
        y,sr = librosa.load(input_wav,sr=origin_sr)
        resample_data = librosa.resample(y,sr,resample_sr)
        sf.write(input_wav,resample_data,resample_sr,subtype='PCM_16')
        #print(f"{input_wav.split('/')[-1]} 파일 {origin_sr} hz -> {resample_sr} hz 샘플링 레이트 변환 완료")
        return

    def convert_channel_to_mono(self,metadata):
        input_wav = metadata['filepath']
        sample_rate = metadata['streaminfo']['sample_rate']
        origin_ch = metadata['streaminfo']['channels']
        y,sr = librosa.load(input_wav,sr=sample_rate)
        y_mono = librosa.to_mono(y)
        #sf.write('convert_channel.wav',y_mono,sr,subtype='PCM_16')
        sf.write(input_wav,y_mono,sr,subtype='PCM_16')
        return

    def remove_unsatisfied_duration_wavs(self):
        print(f'{len(CheckAudio.invalid_duration)} data will be removed') 
        user_ans = input('Do you want to preceed? (y/n) ')
        while 1:
            if user_ans == 'y':
                for key in tqdm(CheckAudio.invalid_duration):
                    os.remove(key)
                return
            elif user_ans == 'n':
                return
            else:
                user_ans = input('rewrite your answer (y or n) ')

    
    def use_config_file(self,config_name):
        json_file = self.config_file+'/'+config_name+'.json'
        if os.path.isfile(json_file):
            with open(json_file,'r',encoding='utf-8') as f:
                json_data = json.load(f)
            return json_data
        else:
            return

    def flag_check(self):

        if self.sr_flag == True:
            print(f'{self.sr} hz sample rate 변환 시작')
            for key in tqdm(CheckAudio.invalid_rate):
                metadata = audio_metadata.load(key)
                self.resampling_rate(self.sr,metadata)
            print("sample rate 변환 완료")
            
        if self.c_flag == True:
            print(f'channels 변환 시작')
            for key in tqdm(CheckAudio.invalid_channels):
                metadata = audio_metadata.load(key)
                self.convert_channel_to_mono(metadata)
            print("channels 변환 완료")

        if self.remove_flag == True:
            self.remove_unsatisfied_duration_wavs()

        return

    def check_routine(self):
        if os.path.exists(self.config_file):
            CheckAudio.invalid_rate = self.use_config_file('invalid_rate')
            CheckAudio.invalid_channels = self.use_config_file('invalid_channels')
            CheckAudio.invalid_duration = self.use_config_file('invalid_duration')
        else:
            for wav in tqdm(self.wav_list):
                meta = self.audio_info(wav)
                self.check_sample_rate(self.sr,meta)
                self.check_channel(self.channels,meta)
                self.check_duration(self.min_d,self.max_d,meta)
            self.write_result(self.config_file)
        
        self.flag_check()            
            
        return


    

def main():
    args = get_args()

    sr = args.sample_rate
    channels = args.channels
    min_d = args.min_duration
    max_d = args.max_duration
    convert_sr_flag = args.convert_sample_rate
    convert_c_flag = args.convert_channels
    remove_flag = args.remove_failed_wav
    config_file = args.config_path

    if args.input_wav_path is None :
        f = sys.stdin
    else :
        assert os.path.exists(args.input_wav_path)
        wavs = get_wav_files(args.input_wav_path)
        preprocess_audio = CheckAudio(sr,channels,min_d,max_d,convert_sr_flag,convert_c_flag,remove_flag,config_file,*wavs)
        preprocess_audio.check_routine()


    return




        
    

if __name__ == "__main__":

    main()
