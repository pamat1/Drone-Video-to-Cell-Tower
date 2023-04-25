# Installation

This installation guide assumes you are working an Nvidia Jetson Nano and a Quecetel EG25-G Cellular Modem.  Steps may apply to other platforms but have not been tested.

## Prerequisites

1. Jetpack 4.6.3 upgraded to Ubuntu 20.04
2. Python 3 is installed on the system
3. GCC and relevant base libraries are installed

## Install Steps

### 1. Install Cell Modem Driver
We will use a provided Github Library that containes the necessary drivers for the EG25-G
```
$git clone https://github.com/mckouba/EG25-G_Setup.git
$cd EG25-G_Setup
#for kernel versions < 5.15
$cd EG25-driver/05_Driver/QMI_WWAN_5.14
#for kernel versions > 5.15
$cd EG25-driver/05_Driver/QMI_WWAN_5.16
#sudo ./make install
```
### 2. Install SRT
Go to SRT github and install > 1.4.x -> [Haivision SRT GitHub](https://github.com/Haivision/srt)

### 3. Upgrade Gstreamer version
```
$sudo apt update
$sudo apt remove *gstreamer*
$sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
#verify version is 1.16.3
$gst-inspect-1.0 --version
```
We need to use Gstreamer version 1.16.3 as the bad plugins package comes packaged with SRT supprt.  We would like to use newer versions as they contain imporvements for the SRT plugin, but there is no hardware support on the Jetson Nano for versions greater than 1.16.3.

### 4. Clone this repo
```
$git clone https://github.com/pamat1/Drone-Video-to-Cell-Tower.git
```


# How to use this code

## On the sender

In the *'Sender'* folder, **drone.py** holds all the code that the drone will run to connect to the server, establish a peer-to-peer connection, and start a stream of video and sensor data. If you are using different I/O for an IMU, **PeripheralFunction.py** should be changed. The **streamfull.sh** and **streamfull_hw.sh** scripts can be changed to try out different pipelines.

```
$python3 Drone-Video-to-Cell-Tower/Sender/drone.py
```

## On the recieving client

The *'Receiver'* code holds the python scripts to be run on the receiver device. **GUI_Test.py** should be run here. **constants.py** holds the address information of the middleman server, as well as options for setting up what ports to stream and chat on. **A copy of this file should be placed in the 'Sender' folder.**

```
$python3 Drone-Video-to-Cell-Tower/Receiver/GUI_Test.py
```

## On the middleman server

The *'Server'* folder holds the relevant script to be run on a server to listen for a pair of clients and help connect them.
```
$python3 Drone-Video-to-Cell-Tower/Server/server.py
```
