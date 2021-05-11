# Set these according to system parameters
PORT        = "/dev/ttyUSB0"
#"/dev/ttyUSB0"                        # Serial port Arduino is connected to
BAUDRATE    = 9600                          # Baud rate Arduino is set to


# Constant Values
GRAVITY     = 9.8                           # Acceleration Due to Gravity
MASS        = 4.99                          # Mass of the drop weight
RADIUS      = 1.4                         # Radius of spool in inches
RADIUS_M    = 0.035                         # Radius of spool in meters
FLAGWIDTH   = 12.7                          # Width of flag in millimeters
CONVERSION  = 39.370                        # Divide by to get metric from us
                                            # Multiply by to get us from metric
CONVERSIONF = 3.2808399                     # Multiply by to get feet from meters
                                            # Divide by to get meters from feet
