from pyfirmata import Arduino, SERVO
from win32com.client import Dispatch


def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)
port='COM10'

pin=10
pin1=7

board=Arduino(port)

led1=board.get_pin('d:8:o')
led2=board.get_pin('d:9:o')

board.digital[pin].mode=SERVO
board.digital[pin1].mode=SERVO

def rotateServo(pin, angle):
    board.digital[pin].write(angle)

def doorAutomate(val):
    if val==0:
        rotateServo(pin, 220)
    elif val==1:
        rotateServo(pin, 40)
def handSantizer(val):
    if val==0:
        rotateServo(pin1, 140)
    elif val==1:
        rotateServo(pin1, 40)

def ledControll(val):
    if val==0:
        led1.write(1)
        led2.write(0)
        speak("Door is Open Now")
    elif val==1:
        led1.write(0)
        led2.write(1)
        speak("Door is Closed  Now")
    else:
        led1.write(0)
        led2.write(0)



