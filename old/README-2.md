## Drone GUI
GUI is currently being developed using Tkinter

- P2P connections/chat
  - The 'server.py' program will be run first, which client ('main.py') #1 connects to. While there is only one client connected to the server, the server will act as an echo server.
  - Once another client connects to the server, the server will then facilitate a P2P connection between the two clients. The two clients will open up sockets to each other. The sockets to the server will stay open. While the two clients are connected, text messages can be sent between them.
- Video Streaming
  - Once a P2P connection is established, clicking the 'stream SRT' button on one of the client GUIs will launch a shell script in a separate thread that handles all SRT streaming.
  
### server.py
This file will be run on the server machine. Best practice is to run this program first, get the IP address it is using (it will ping Wikipedia and find it in the reply), and then hardcode that address value into main.py and main_headless.py.
  
### main_headless.py
This file is run on the microprocessor and will automatically connect to the server. After the server establishes a P2P conneciton, it will then start streaming. Sometimes the intended socked is currently in use (probably from a previous instance of the script) and the process with that socket will need to be killed.
