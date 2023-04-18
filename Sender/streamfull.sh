#!/bin/bash

../pipeline_test_kouba.sh
& 	./srt-live-transmit udp://:5000 srt://$1:$2?mode=rendezvous \
&& fg  

