#!/bin/bash

source_dir=$1
target_dir=$2

mkdir -p $target_dir

find $source_dir/ -name "*.wav" | sed "s:$source_dir/::g" |
while read -r f;
do
	base_wav=$(basename $f)
	dirpath=$(dirname $f)
	mv $source_dir/$dirpath/$base_wav $target_dir
done

