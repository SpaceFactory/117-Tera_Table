#!python3
#Import socket module
import socket
import time




# Define the port on which you want to connect
port = 12346

# connect to the server on local computer
s = socket.socket()
s.connect(('192.168.1.61', port))

while True:
 try:
    while True:

       instruct = """{
       "command": "goto",
       "speed":20,
       "point":180
       }"""
       s.send(instruct.encode())
       data = str((s.recv(1024)).decode())
       print('goto command to executed, should cause error if table is already at  ',data)


       time.sleep(5)

       instruct = """{
       "command": "eStop"
       }"""
       s.send(instruct.encode())
       data = str((s.recv(1024)).decode())
       print('estop sent ',data)



       time.sleep(100)

   #s.close()
   #"points": [60,61,62,63,64,65,66,67,68,69,70,71,72,73,80]
   #"points": [89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113]
 except Exception as e:
   print('Got exception and closing connection',e)
   s.close()
   s.connect(('192.168.1.61', port))

s.close()
