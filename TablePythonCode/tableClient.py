#!python3
#Import socket module
import socket
import time




# Define the port on which you want to connect
port = 12346

# connect to the server on local computer
s = socket.socket()
s.connect(('192.168.1.69', port))


try:
   instruct = """{
   "command": "goto",
   "speed": 25,
   "points": [89,99,109,119,129]
   }"""

   s.send(instruct.encode())
   data = str((s.recv(1024)).decode())

   data = ''
   while(data!= '4'):
    s.send("""{"command" : "getCurrentIndex"}""".encode())
    data = str((s.recv(1024)).decode())
    print(data)
    time.sleep(0.25)

   time.sleep(5)
   instruct = """{
   "command": "goto",
   "speed": 25,
   "points": [119,109,99,89]
   }"""
   s.send(instruct.encode())
   data = str((s.recv(1024)).decode())

   data = ''
   while(data!= '3'):
    s.send("""{"command" : "getCurrentIndex"}""".encode())
    data = str((s.recv(1024)).decode())
    print(data)
    time.sleep(0.25)

   s.close()
#"points": [60,61,62,63,64,65,66,67,68,69,70,71,72,73,80]
#"points": [89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113]
except Exception as e:
  print('Got exception and closing connection',e)
  s.close()

finally:
  print('Finally closing connection')
  s.close()
