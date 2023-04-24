
### Using this code

The *'Server'* folder holds the relevant script to be run on a server to listen for a pair of clients and help connect them.

The *'Receiver'* code holds the python scripts to be run on the receiver device. **GUI_Test.py** should be run here. **constants.py** holds the address information of the middleman server, as well as options for setting up what ports to stream and chat on. **A copy of this file should be placed in the 'Sender' folder.**

In the *'Sender'* folder, **drone.py** holds all the code that the drone will run to connect to the server, establish a peer-to-peer connection, and start a stream of video and sensor data. If you are using different I/O for an IMU, **PeripheralFunction.py** should be changed. The **streamfull.sh** and **streamfull_hw.sh** scripts can be changed to try out different pipelines.
