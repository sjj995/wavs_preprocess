from hashlib import new
import os
import glob

dir = './kaist_audio_book_22050/'

dir_list = [f for f in os.listdir(dir)]

dic_file = {
    '남':'male',
    '여':'female',
    '동화':'fairy_tale',
    '소설':'novel',
    '어학':'language',
    '뉴스':'news',
    '자기계발':'self_improvement'
}

#파일명 변경
for dir_name in dir_list:
    for wav_file in os.listdir(dir+dir_name):
        old_name = dir+dir_name+'/'+ wav_file
        new_name = dir+dir_name+'/'+ dir_name+'_'+wav_file
        os.rename(old_name,new_name)
        old_name=''
        new_name=''