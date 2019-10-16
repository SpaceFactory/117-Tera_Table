#!python2.7
from pycomm.ab_comm.clx import Driver as ClxDriver
import logging
import time
from datetime import datetime


_delay = 10
spd = 100


def reset():
    # Reset the drive
    #print("Driver Reset: ", c.write_tag('Drive_1_Command.RESET', 1, 'BOOL'))
    #print("Driver Reset: ", c.write_tag('Drive_1_Command.RESET', 0, 'BOOL'))
    # Stop automatic motion
    # print("Stop  Motion", c.write_tag('Stop_Motion', 1, 'BOOL'))
    _resp = c.read_tag(['Set_Home'])
    if _resp[0][1] == 1:
        print("Stop  Motion", c.write_tag('Stop_Motion', 0, 'BOOL'))
    # Clear Faults
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
    print("Direction:", c.write_tag('Direction_Mode', 2, 'INT'))
    # Set Speeds
    print("Speed: ", 50, c.write_tag(('jog_ST_Speed', 50, 'REAL')))
    print("Speed: ", 50, c.write_tag(('ST_Speed', 50, 'REAL')))
    print("Speed: ", 50, c.write_tag(('time_ST_Speed', 50, 'REAL')))


if __name__ == '__main__':
    logging.basicConfig(
        filename="ClxDriver.log",
        format="%(levelname)-10s %(asctime)s %(message)s",
        level=logging.DEBUG
    )
    c = ClxDriver()

    print("connecting to driver...",)
    if c.open('192.168.1.5'):
        reset()
        # Get position

        while True:
           start_time = datetime.now()
           position = (c.read_tag(['FB_Position']))
           position_angle = position[0][1]

           stop_time = datetime.now()

           print("angle = ",position_angle,(stop_time - start_time))

           #time.sleep(1);




        c.close()
        # print('finally closed connection')
