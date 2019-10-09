#!python3
#Import socket module
import socket
import time




# Define the port on which you want to connect
port = 12346

# connect to the server on local computer
s = socket.socket()
s.connect(('192.168.1.13', port))


try:
   #instruct = """{
   #"command": "goto",
   #"speed": 10,
   #"points": [89,90,91,92,93,94,95]
   #}"""
   #[89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,200.201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,225,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250]
   #print(instruct)
   #s.send(instruct.encode())
   time.sleep(0.5)
   data = ''
   while(data!= 'Completed'):
    print('Sending command getcurrentindex')
    s.send("""{"command"  "getCurrentIndex"}""".encode())
    print('sent')
    data = (s.recv(1024)).decode()
    print(data)
    time.sleep(2)
   s.close()
#"points": [60,61,62,63,64,65,66,67,68,69,70,71,72,73,80]
#"points": [89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113]
except Exception as e:
  print('Got exception and closing connection',e)
  s.close()

finally:
  print('Finally closing connection')
  s.close()
