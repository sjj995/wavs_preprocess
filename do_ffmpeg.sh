#!/bin/bash
sample_rate=$1
src_dir=/datadrive/vocoder/origin_data/youtube_origin5
target_dir=/datadrive/vocoder/22k/youtube_22k_5


file_list=`find $src_dir -name "*.wav" | sed "s:$src_dir/::g"` 

for file in $file_list;
do
    #echo $file
    ffmpeg -i $src_dir/$file -c:a pcm_s16le -ar $sample_rate -ac 1 $target_dir/$file 
done

