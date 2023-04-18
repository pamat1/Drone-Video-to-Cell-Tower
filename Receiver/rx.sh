#!/bin/bash

srt-live-transmit srt://$1:$2?mode=rendezvous file://con | ffplay -f mpegts -
