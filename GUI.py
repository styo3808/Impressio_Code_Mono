
#
#   Author: Stanley A Young
#   Date: 06-15-2020
#   Title: GUI.py
#
#   Description:
#       Produces a graphical user interface for Impressio project
#


# Libraries
import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import const


class GUI:

    def __init__(self, serialObject):
        """
        The __init__ method takes a Serial object, calls the initializeRootWindow,
        initializeLables, initializeButtons passing the Serial object as an argument, and
        the geometryManagement methods on itself.
        """
        # private class variables
        self.root       = tk.Tk()
        self.height     = tk.StringVar(value="Height:")
        self.energy     = tk.StringVar(value="Energy:")
        self.unit       = tk.StringVar(value="Metric")

        self.notifications = 0

        self.initializeRootWindow()
        self.initializeLabels()
        self.initializeButtons(serialObject)
        self.geometryManagement()


    def initializeRootWindow(self):
        """
        The initializeRootWindow method calls the title, geometry, , configure, and resizable
        method on the root private variable inside self.
        """
        self.root.title("Impressio Monorail")
        self.root.geometry("800x400")
        self.root.configure(background='blue')
        self.root.resizable(False, False)


    def initializeLabels(self):
        """
        The initializeLabels method creates two labels using the tkinter ttk module and
        puts those two labels in the root window with the grid geometry manager.
        """
        self.heightLabel = tk.ttk.Label(self.root, textvariable=self.height,
                                        relief="solid", font="Times 22 bold",
                                        anchor=tk.CENTER, width=10)
        self.heightLabel.grid(row=0, column=0, sticky='nsew')

        self.energyLabel = tk.ttk.Label(self.root, textvariable=self.energy,
                                        relief="solid", font="Times 22 bold",
                                        anchor=tk.CENTER, width=10)
        self.energyLabel.grid(row=0, column=1, sticky='nsew')


    def initializeButtons(self, serialObject):
        """
        The initializeButtons method builds three buttons in the root window using the
        tkinter ttk module packing them with the grid geometry manager and connecting them
        to their relative functions with the Serial object.
        """

        ttk.Button(self.root, text="Set Floor",
                   command=lambda: self.setFloor(serialObject)).grid(
                       row=1, column=0, sticky='nsew', padx=5, pady=5,
                        columnspan=2)

        ttk.Button(self.root, text="Exit",
                    command=lambda: self.exit(serialObject)).grid(
                        row=3, column=0, sticky='sw', padx=10, pady=10)

        ttk.Button(self.root, textvariable=self.unit,
                    command= lambda: self.changeUnit(serialObject)).grid(
                        row=3, column=1, sticky='se',padx=10, pady=10)


    def geometryManagement(self):
        """
        The geometryManagement method sets all the rows and columns of the root window to
        resize at the same rate as the root window.
        """
        for i in range(3):
            self.root.rowconfigure(i, weight=1)

        for i in range(2):
            self.root.columnconfigure(i, weight=1)


    # Button Events
    def setFloor(self, serialObject):
        """
        The setFloor method is called whenever the button labelled 'Set Floor' is pressed.

        The setFloor method writes an 'f' character to the serial port.
        """
        serialObject.write(b'f')
        return


    def changeUnit(self, serialObject):
        """
        The changeUnit function is the callback for the unit button
        """
        current = self.unit.get()

        if(current == "Metric"):
            self.unit.set("U.S.")
        else:
            self.unit.set("Metric")

        serialObject.write(b'c')

        return


    def exit(self, serialObject):
        """
        The exit method is called whenever the button labelled 'Exit' is pressed.

        The exit method calls the destroy method of the root private variable inside itself.
        """
        serialObject.write(b's')
        self.root.destroy()

        return


    # Other functions
    def notify(self):
        self.notifications += 1

        if(self.notifications == 1):
            messagebox.showinfo(title = 'Loading...', message = 'Close this message and rotate the encoder until all pins have been found')
        elif(self.notifications > 100):
            messagebox.showinfo(title = 'Illegal Pin Config', message = 'Something is wrong with the pin configuration. Close this message, check encoder connection and try again.')
            return False

        return True


    def updateHeight(self, height):
        """
        The updateHeight method takes a height sets the stringVar in the height label to
        that height eased in feet and inches.
        """
        currentUnit = self.unit.get()

        if(currentUnit == "Metric"):
            if (height >= 0):
                inches  = height % 12
                feet    = int(height // 12)
            else:
                inches  = -((-height) % 12)
                feet    = -int((-height) // 12)

            self.height.set("Height: {}' {}\"".format(
                feet, round(inches, 1)))
        else:
            self.height.set("Height: {} m".format(
                round(height / const.CONVERSION, 3)))

        return


    def updateEnergy(self, energy):
        """
        The updateEnergy method takes an energys sets the stringVar in the energy label
        to that energy eased in joules.
        """

        self.energy.set("Energy: {} j".format(round(energy, 2)))

        return


    def updateWindow(self, height = None):
        """
        The updateWindow method calls the update method of the root private variable of self.
        """
        try:
            self.root.update()
        except tk.TclError:
            return False

        if(height != None):
            self.updateHeight(height)
            self.updateEnergy((height / const.CONVERSION) *
                              const.GRAVITY * const.MASS)
            self.root.update()

        return True
