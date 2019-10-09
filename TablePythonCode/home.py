#!python2.7
from pycomm.ab_comm.clx import Driver as ClxDriver
import logging
import time
from reset import reset

_delay = 10
spd = 50

if __name__ == '__main__':
    logging.basicConfig(
        filename="ClxDriver.log",
        format="%(levelname)-10s %(asctime)s %(message)s",
        level=logging.DEBUG
    )
    c = ClxDriver()

    print("Connecting to Motor",)
    if c.open('192.168.1.5'):
        print("Success")
        reset(c)

        # Set to home
        print("Setting Home: ", c.write_tag(('Set_Home', 1, 'BOOL')))
        print(c.write_tag('Direction_Mode', 3, 'INT'))
        print(c.write_tag('Goto_Deg', 0.1, 'REAL'))
        print(c.write_tag('GT_Start_Req', 1, 'BOOL'))
    c.close()
    print('closed connection')
