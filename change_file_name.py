from operator import contains
import os

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

#디렉터리명만 변경
#파일명에서 여러개의 요소를 바꿀 때 사용
#ex. 남1_동화 -> male1_동화 -> male1_fairy_tale
for dir_name in dir_list:
    cnt = 0
    for k,v in dic_file.items():
        res = dir_name.find(k)
        if res != -1:
            tmp_name = dir_name.replace(k,v)
            if cnt == 0: # 경로까지 포함해서
                new_name = dir + tmp_name
                old_name = dir + dir_name
                cnt += 1
            elif cnt != 0:
                new_name = tmp_name
                old_name = dir_name
            dir_name = new_name
            os.rename(old_name,new_name)
     