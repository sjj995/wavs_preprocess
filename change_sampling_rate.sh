#!/bin/bash
#sampling rate,bit rate, channel 변경

source_dir=$1
target_dir=$2

find $source_dir/ -name "*.wav" | sed "s:$source_dir/::g" |
while read -r f;
do
    base_wav=$(basename $f)
    dirpath=$(dirname $f)
    mkdir -p $target_dir/$dirpath
    #sox $source_dir/$dirpath/$base_wav -b 16 -c 1 -r 22050 $target_dir/$dirpath/$base_wav
    sox $source_dir/$base_wav -t wav -b 16 -c 1 -r 22050 $target_dir/$base_wav
    echo "변환중인 파일 : => $target_dir/$base_wav"
done
