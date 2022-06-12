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
        help="remove unsatisfied duration files(Default: false)",
    )

    parser.add_argument(
        "-m",
        "--merge_wav_file",
        type=boolean,
        help="merge wav file in one directory(Default: false)",
    )

    parser.add_argument(
        "-csr",
        "--convert_sample_rate",
        type=boolean,
        help="convert sample rate(Default: false)",
    )

    parser.add_argument(
        "-cc",
        "--convert_channel",
        type=boolean,
        help="convert channel to mono(Default: false)",
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

    def __init__(self,sr,channels,min_d,max_d,*wavs):
        self.sr = sr
        self.channels = channels
        self.min_d = min_d
        self.max_d = max_d
        self.wav_list = wavs
    
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
        elif metadata['streaminfo']['duration'] > max_d:  
            CheckAudio.invalid_duration[metadata['filepath']] = metadata['streaminfo']['duration']
            #print(f"duration is too long!!\n file : {metadata['filepath']}")
        else:
            pass
            #print("duration check complete")
        return

    def write_result(self,path):
        
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

    def check_routine(self):
        for wav in self.wav_list:
            meta = self.audio_info(wav)
            self.check_sample_rate(self.sr,meta)
            self.check_channel(self.channels,meta)
            self.check_duration(self.min_d,self.max_d,meta)
        

            self.write_result(os.getcwd())
        return




def main():
    args = get_args()

    sr = args.sample_rate
    channels = args.channels
    min_d = args.min_duration
    max_d = args.max_duration

    if args.input_wav_path is None :
        f = sys.stdin
    else :
        assert os.path.exists(args.input_wav_path)
        wavs = get_wav_files(args.input_wav_path)
        preprocess_audio = CheckAudio(sr,channels,min_d,max_d,*wavs)
        preprocess_audio.check_routine()

    # if args.output is None :
    #     fw = sys.stdout
    # else :
    #     fw = open(args.output, "w")



        


if __name__ == "__main__":

    main()
