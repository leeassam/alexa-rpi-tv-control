'''
Application for testing ir signals to your tv from python using irsend
irsend : http://www.lirc.org/html/irsend.html

Created by: Lee Assam
www.powerlearningacademy.com

Last Modified: 2018-07-20
'''
import argparse, os, time

'''
-- Program for quickly testing your remote --
#Command line arguments
#Usage: python3 test.py power on
#Usage: python3 test.py volume increase

#Turning your tv on or off
power on
power off

#Adjusting your volume
volume increase
volume decrease
volume mute
volume unmute

#Switching to a specific channel
channel 35

#Channel Surfing
surf up
surf down

'''

#Specify the name of your TV that was configured in the lircd.conf file
device = "sony"

#getting the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("control", help="What you want to control [volume | power | channel | surf]")
parser.add_argument("action", help="How you want to adjust the control [increase | decrease]")
args = parser.parse_args()

#Extracting the arguments
control = args.control
action = args.action

#Debug
print(control)
print(action)

#sends a repeating command
#see the irsend command in lirc documentation http://www.lirc.org/html/irsend.html
#command : The IR command to execute
#duration : The duration in seconds to sleep/pause while the command is being repeated
def sendRepeatCommand(command, duration):
    os.system("irsend SEND_START {} {} ; sleep {}".format(device, command, duration))
    os.system("irsend SEND_STOP {} {}".format(device, command))

#adjust power
if control == "power":
    os.system("irsend --count=2 SEND_ONCE %s KEY_POWER KEY_POWER" % device)

#adjust volume
elif control == "volume":
    if action == "increase":
        sendRepeatCommand("KEY_VOLUMEUP", 3)
    elif action == "decrease":
        sendRepeatCommand("KEY_VOLUMEDOWN", 3)
    elif action == "mute" or action == "unmute":
        sendRepeatCommand("KEY_MUTE", 0.1)

#switch to a specific channel
elif control == "channel":
    channelNums = list(str(action))
    for i in channelNums:
        sendRepeatCommand("KEY_" + i, 0.1)
        time.sleep(0.5)
        
#channel surf
elif control == "surf":
    if action == "up":
        sendRepeatCommand("KEY_CHANNELUP", 0.1);
    elif action == "down":
        sendRepeatCommand("KEY_CHANNELDOWN", 0.1);
    elif action == "stop":
        #exit
        print("Stopping")
