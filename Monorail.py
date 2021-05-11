#
#   Author: Stanley A Young
#   Date: 02-11-2021
#   Title: Twin_Wire.py
#
#   Description:
#   Graphical user interface and serial communication handlers for
#   Impressio twin-wire impact testing equipment height measurement
#   system.
#

# Libraries
import const
import GUI as G
from serial import *

# Functions
def main():
    """
    The main function is the main driver for the program and will be called on entry.
    """

    # Initialize the Serial Port
    try:
        serialPort  = Serial(const.PORT, const.BAUDRATE)
    except serialutil.SerialException:
        print("port inaccessable at this time")
        return -1

    # Initialize the GUI
    mainWindow = G.GUI(serialPort)

    while(1):
        if(not mainWindow.updateWindow()): break
        # Check the Serial port receive buffer for data
        if (serialPort.in_waiting > 0):

            # Read in the first byte of data and decode it to a string
            byte = serialPort.read()
            flag = byte.decode("utf-8")

            # flag l indicates that the pins have not been found
            # message user to spin the motor until pins are initialized
            if(flag == 'l'):
                if(not mainWindow.notify()): break

            # flag h indicates a height measurement is being transferred
            # gather data in local storage and display to the screen
            elif(flag == 'h'):
                line = serialPort.readline()
                string = line.decode("utf-8")
                stripped = string.rstrip()
                value    = float(stripped)
                if(not mainWindow.updateWindow(value)): break

            # close out program and notify user in terminal of error in firmware
            elif(flag == 'e'):
                print("An error occured in the firmware on the microcontroller")
                break

            # this is an error state
            # print error message to console and exit
            else:
                print(flag)
                print("An unexpected flag was raised")


    # When loop exits, close the Serial port
    serialPort.close()


if __name__ == "__main__": main()



