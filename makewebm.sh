src_dir=/datadrive/vocoder/autoscript
target_dir=/datadrive/vocoder/origin_data/youtube_origin6
textfile=youtubeurl6.txt

while read -r f; 
do
    url=$(echo $f | awk '{print $1}')
    file_name=$(echo $f | awk '{print $2}')
    flist=$(youtube-dl -F "$f" | sed -n '5,10p' | awk '{print $1}')
    for format in $flist;
    do
        if [ $format -eq 251 ];then
            #echo $format
            youtube-dl -f "$format" "$url" -o $target_dir/$file_name&
            break
        
        elif [ $format -eq 250 ];then
            #echo $format
            youtube-dl -f "$format" "$url" -o $target_dir/$file_name&
            break
        
        elif [ $format -eq 140 ];then
            #echo $format
            youtube-dl -f "$format" "$url" -o $target_dir/$file_name&
            break
        
        elif [ $format -eq 249 ];then
            #echo $format
            youtube-dl -f "$format" "$url" -o $target_dir/$file_name&
            break
        fi
    done
done < $src_dir/$textfile
