import os
import glob
import math
import random
import shutil
# 텍스트파일 또는 wav파일 train dataset과 test dataset으로 나누는 모듈

working_dir='audio_book_22050'
destination_dir=['train','test','val']
ratio=[0.8,0.2] # train,test,validation, ex, [0.8,0.15,0.05]
is_val=False


filelist = os.listdir(working_dir)

len_train_dataset = int(round(len(filelist) * ratio[0]))
idx = [i for i in range(1,len(filelist)+1)]
if is_val is True:
    len_val_datset = int(round(len(filelist) * ratio[2]))
    len_test_dataset = len(filelist) - len_train_dataset  - len_val_datset

    train_idx = random.sample(idx,len_train_dataset)
    train_dataset = [filelist[i-1] for i in train_idx]
    test_val_idx = list(set(idx) - set(train_idx))

    test_idx = random.sample(test_val_idx,len_test_dataset)
    test_dataset = [filelist[i-1] for i in test_idx]
    val_idx = list(set(test_val_idx) - set(test_idx))
    val_dataset = [filelist[i-1] for i in val_idx]

else:
    len_test_dataset = len(filelist) - len_train_dataset

    train_idx = random.sample(idx,len_train_dataset)
    train_dataset = [filelist[i-1] for i in train_idx]

    test_idx = list(set(idx) - set(train_idx))
    test_dataset = [filelist[i-1] for i in test_idx]


dataset = [train_dataset,test_dataset,val_dataset]

if is_val is False:
    destination_dir = destination_dir[:-1]
    dataset = [train_dataset,test_dataset]


for destination in destination_dir:
    file_destination = working_dir+'/'+destination

    if not os.path.exists(file_destination):
        os.makedirs(file_destination)

    for data in dataset:
        for wav in data:
            shutil.move(working_dir+'/'+wav,file_destination)


    # with open(file_destination+'/'+destination+'.txt','w',encoding='utf-8') as f:
    #     f.write(file_destination+'/'+wav)



# for i in train_dataset:
#     if i in test_dataset:
#         print("train and test 겹침")
#     elif i in val_dataset:
#         print("train val 겹침")
