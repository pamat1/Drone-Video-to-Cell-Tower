#!/bin/bash

while true
do
gst-launch-1.0 -v \
          filesrc location=/home/xavier/test4kvideo.mp4 \
        ! qtdemux \
        ! h264parse \
        ! nvv4l2decoder \
        ! nvv4l2h265enc control-rate=constant_bitrate \
        ! mpegtsmux \
        ! srtsink uri="srt://0.0.0.0:9854?mode=listener"
done
