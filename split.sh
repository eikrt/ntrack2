ffmpeg -i samples/korg1/main.wav -acodec copy -f segment -segment_time 1 -vcodec copy -reset_timestamps 1 -map 0 samples/korg1/output_time_%d.wav
