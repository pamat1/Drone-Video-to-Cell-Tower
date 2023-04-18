#!/bin/bash

ffmpeg -re -i "lions.mp4"  -f lavfi -re \
	  -i sine=frequency=1000:duration=60:sample_rate=44100 -pix_fmt yuv420p \
	  -c:v libx264 -b:v 1000k -g 30 -keyint_min 120 -profile:v baseline \
	  -preset veryfast -f mpegts "udp://127.0.0.1:5000?pkt_size=1316" \
& 	./srt-live-transmit udp://:5000 srt://$1:$2?mode=rendezvous \
&& fg  

