#!python3
#Import socket module
import socket
import time




# Define the port on which you want to connect
port = 12346

# connect to the server on local computer
s = socket.socket()
s.connect(('192.168.1.69', port))

while True:
 try:
    while True: n 
       instruct = """{
       "command": "goThroughPoints",
       "speed":30,
       "points":[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270]
       }"""
       s.send(instruct.encode())
       data = str((s.recv(1024)).decode())
       print('goto command to executed going from 0 to 270 and stop at 60 ',data)


       while True:
           instruct = """{
           "command": "getCurrentIndex"
           }"""
           s.send(instruct.encode())
           data = str((s.recv(1024)).decode())
           if(data == '6'):
               instruct = """{
               "command": "eStop"
               }"""
               s.send(instruct.encode())
               break
           time.sleep(0.05)

       print('resuming from 60 to 270 after 30 sec')
       time.sleep(30)

       instruct = """{
       "command": "goThroughPoints",
       "speed":30,
       "points":[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270]
       }"""
       s.send(instruct.encode())
       data = str((s.recv(1024)).decode())
       print('goto command to executed going from 60 to 270 ',data)




       time.sleep(1000)

   #s.close()
   #"points": [60,61,62,63,64,65,66,67,68,69,70,71,72,73,80]
   #"points": [89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113]
 except Exception as e:
   print('Got exception and closing connection',e)
   s.close()
   s.connect(('192.168.1.69', port))

s.close()
