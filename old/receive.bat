@echo off
if [%1]==[] goto eof
start "" "C:\Program Files\VideoLAN\VLC\vlc.exe" "srt://%1?mode=caller"
:eof
