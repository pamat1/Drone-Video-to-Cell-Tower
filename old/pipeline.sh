#!/bin/bash

if [ $# -eq 0 ] #make sure there is at least one arguement.  Should add more checking, but good enoug for now
then
          echo "No port provided. Exiting..."
          exit 1
fi

while true
do
gst-launch-1.0 -v \
          filesrc location=/home/jetson/test4kvideo.mp4 \
        ! qtdemux \
        ! h264parse \
        ! nvv4l2decoder \
        ! nvv4l2h265enc control-rate=constant_bitrate \
        ! mpegtsmux \
        ! srtsink uri="srt://0.0.0.0:$1?mode=listener"
done
