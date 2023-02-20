@echo off
if [%1]==[] goto eof
start "" "C:\Program Files\VideoLAN\VLC\vlc.exe" "%1"
:eof