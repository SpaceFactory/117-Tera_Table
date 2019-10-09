#!python2.7
from pycomm.ab_comm.clx import Driver as ClxDriver
import threading
import logging
import socket
import json
import time
import sys


'''
    This program has two threads:
        - Thread 1: handles socket communication over the network.
        - Thread 2: handles communication to the PLC
'''

# Section related to socket communication
s = socket.socket()
port = 12346
s.bind(('', port))
s.listen(1)

# some global variables for the PLC Thread
plc_ip_address = '192.168.1.5'
accuracy_desired = 0.05  # accuracy desired in degree
message_json = None
command = None

logging.basicConfig(
        filename="ClxDriver.log",
        format="%(levelname)-10s %(asctime)s %(message)s",
        level=logging.DEBUG
    )

# initialize the communication driver
# this is a global variable that will only be used from the second thread.
c = ClxDriver()

# used to track the last index reached in the table motion vector
curr_index = -1


def reset():
    '''
        This is called by one of the motion options in the PLC thread.
        :. It must already by opened when the function is called.
    '''
    print("Driver Reset: ", c.write_tag(
        'Drive_1_Command.RESET', 1, 'BOOL'))
    print("Driver Reset: ", c.write_tag(
        'Drive_1_Command.RESET', 0, 'BOOL'))
    # Stop automatic motion
    print("Stop  Motion", c.write_tag('Stop_Motion', 1, 'BOOL'))
    print("Stop  Motion", c.write_tag('Stop_Motion', 0, 'BOOL'))

    _resp = c.read_tag(['Set_Home'])
    if _resp[0][1] == 1:
        print("Stop  Motion", c.write_tag('Stop_Motion', 0, 'BOOL'))
    # Clear Faultsdd
    print("Fault Active?:", c.read_tag(['Fault_Active']))
    _resp = c.read_tag(['Set_Home'])
    if _resp[0][1] == 1:
        print("Fault HIGH:", c.write_tag('Clear_Fault', 1, 'BOOL'))
        print("Fault LOW:", c.write_tag('Clear_Fault', 0, 'BOOL'))

    # Confirm No Active Faults
    print("Fault Active?:", c.read_tag(['Fault_Active']))
    # Disable Jog
    print("Disable Jog: ", c.write_tag('J_Start_Req', 0, 'BOOL'))
    # Disable Timed
    print("Disable Timed: ", c.write_tag('T_Start_Req', 0, 'BOOL'))
    # Disable Go To Move
    print("Disable GoTo: ", c.write_tag('GT_Start_Req', 0, 'BOOL'))
    # Disable Relative
    print("Disable Relative: ", c.write_tag('R_Start_Req', 0, 'BOOL'))
    # disable alrt
    print("Disable Relative: ", c.write_tag('Alt_Start_Req', 0, 'BOOL'))
    # Set Direction to Clockwise
    # 2-counter-clockwise,  1-clockwise,   3-shortestpath to a position
    print("Direction:", c.write_tag('Direction_Mode', 1, 'INT'))
    # Set Speeds
    print("Speed: ", 50, c.write_tag(('jog_ST_Speed', 50, 'REAL')))
    print("Speed: ", 50, c.write_tag(('ST_Speed', 50, 'REAL')))
    print("Speed: ", 50, c.write_tag(('time_ST_Speed', 50, 'REAL')))
    # if home is 1 set to 0
    _resp = c.read_tag(['Set_Home'])
    if _resp[0][1] == 1:
        print("Setting Home: ", c.write_tag(('Set_Home', 0, 'BOOL')))


def gotoMotion(angle, speed, direction):
    try:
        c.open(plc_ip_address)
        reset()
        print("Direction:", c.write_tag('Direction_Mode', direction, 'INT'))
        print("Speed: ", speed, c.write_tag(('ST_Speed', speed, 'REAL')))
        print(c.write_tag('Goto_Deg', angle, 'REAL'))
        print(c.write_tag('GT_Start_Req', 1, 'BOOL'))
        c.close()
        return True

    except Exception as e:
        print('Exception encountered in gotoMotion ',e)
        return False


def relativeMotion(angle, speed):
    try:
        c.open(plc_ip_address)
        reset()
        print('Inside relative function')
        # direction is not presently declared
        print("Direction:", c.write_tag('Direction_Mode', direction, 'INT'))
        print("Speed: ", speed, c.write_tag(('ST_Speed', speed, 'REAL')))
        print(c.write_tag('Rel_Deg', angle, 'REAL'))
        print(c.write_tag('R_Start_Req', 1, 'BOOL'))
        c.close()
        return True

    except Exception as e:
        print('Exception encountered in relativeMotion',e)
        return False


def setHome():
    try:
        c.open(plc_ip_address)
        reset()
        print('Inside setHome function')
        print("Setting Home: ", c.write_tag(('Set_Home', 1, 'BOOL')))
        c.close
        return True

    except:
        print('Exception encountered in setHome ',e)
        return False


# reads the current position, if cannopt returns False
# make sure the connection is opened and closed from the code Section
# where readposition is called
def readPosition():
    try:
        # print('Inside readPosition function')
        position = (c.read_tag(['FB_Position']))
        position_angle = position[0][1]
        # print('position angle = ',position_angle)
        return position_angle

    except:
        print('Exception encountered in readPosition')
        return False


# resets the driver
def resetDriver():
    try:
        c.open(plc_ip_address)
        reset()
        c.close()
        return True
    except:
        print('Exception encountered in resetDriver')
        return False

# popTargetPoint() returns two lists: one of the point(s) that was passed,
# and one of the points remaining to be passed by the table.
# This definition ensures that no point is skipped,
# even if network latency occurs. - JC


def popTargetPoint(_min, _diffs, _points):
    if len(_diffs) != len(_points):
        return "ERROR"
    _completed = []  # the points, as an array, popped from the list
    _remaining = []  # the remaining points to be executed
    for i, d in enumerate(_diffs):
        if d == _min:
            # if the differnce is the smallest in the set
            _completed = _points[:i+1]
            _remaining = _points[i+1:]
    return _completed, _remaining


def motionControl():
    global command
    global message_json
    global curr_index
    while True:
        #print('"', command, '"')
        if command is not None:
            # if command is goto
            if(command == 'goto'):
                curr_index = -1
                speed = message_json['speed']
                points = message_json['points']
                stop_point = points[-1]

                # Finding clk/anti-clk direction through 4 consecutive points
                diff1 = 1 if (points[1] - points[0]) > 0 else -1
                diff2 = 1 if (points[2] - points[1]) > 0 else -1
                diff3 = 1 if (points[3] - points[2]) > 0 else -1
                direction = 1 if (diff1 + diff2 + diff3) > 0 else 2

                returned_value = gotoMotion(stop_point, speed, direction)
                conn.send(str(returned_value).encode())

            # if command is relative
            elif(command == 'relative'):
                speed = message_json['speed']
                angle = message_json['relative_angle']
                # setting final_position value not to be -ve or above 360
                if((initial_position + angle) > 360):
                    final_position = (initial_position + angle) - 360
                elif((initial_position + angle) < 0):
                    final_position = (initial_position + angle) + 360
                else:
                    final_position = (initial_position + angle)
                returned_value = relativeMotion(angle, speed)
                command = None
                conn.send(str(returned_value).encode())

            #  if command is  setHome
            elif(command == 'setHome'):
                returned_value = setHome()
                command = None
                conn.send(str(returned_value).encode())

            # if command is reset
            elif(command == 'reset'):
                returned_value = resetDriver()
                command = None
                conn.send(str(returned_value).encode())

            # if command is getPosition
            elif(command == 'getPosition'):
                returned_value = resetDriver()
                command = None
                conn.send(str(returned_value).encode())

            # # if command is getPosition
            # elif(command == 'getCurrentIndex'):
            #     global curr_index
            #     print(curr_index)
            #     returned_value = resetDriver()
            #     command = None

            # if command is other
            else:
                print('No proper command sent')
                returned_value = False
                command = None
                conn.send(str(returned_value).encode())

            # sending periodic updates if the command is goto
            if (returned_value and command == 'goto'):
                _points = message_json['points']  # an array of points
                _completed = [0]
                _remaining = points
                final_position = _points[-1]

                c.open(plc_ip_address)
                current_position = readPosition()
                while(abs(final_position - current_position) > accuracy_desired):
                    # right now the program doesn't identify WHICH point has been reached
                    # just that it was CLOSE to one of them
                    diff = [180-abs(abs(x-current_position) - 180)
                            for x in _points]
                    _min = min(diff)
                    if(_min <= accuracy_desired):
                        _completed, _points = popTargetPoint(_min, diff, _points)
                        print('Completed ', _completed)
                        curr_index =  points.index(_completed[-1])
                    current_position = readPosition()
                    time.sleep(0.01)
                    # At this point the table has completed a full wall Section
                curr_index =  points.index(_completed[-1])
                c.close()
                returned_value = False
                command = None

        else:
            # wait and check again
            # as not to waste too many cycles on None
            time.sleep(0.05)


#gotoMotion(88, 100, 3)
#t.start()
print('Thread started sucessfully waiting for connection')
# Establish connection with client by accepting client request to connect.
conn, addr = s.accept()
print("True")

while True:
    try:

        # conn, addr = s.accept()

        # size of data chunk read at a time in bytes
        data = conn.recv(1024)
        #print('data received from client before parsing as json ', data)
        # convert data to string and  to json
        message_json = json.loads(str(data))
        command = message_json['command']

        if command == 'getCurrentIndex':
           #print("request from robot ")
           conn.send(str(curr_index).encode())
           #print('finished sending to client')
    except socket.error as e:
        print('Socket error exception ',e)
        #stop/reset table in case of error
        resetDriver()
        conn.close()
        conn, addr = s.accept()

    except KeyError as e:
        print('Key error exception ', e)
        #stop/reset table in case of error
        resetDriver()
        #send value -1 to indicate False or error
        conn.send('-1'.encode())

    except Exception as e:
        print('inside final exception ', e)
        #stop/table in case of error
        resetDriver()
        #send value -1 to indicate False or error
        conn.send('-1'.encode())
