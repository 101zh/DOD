"""CircuitPython Essentials Servo standard servo example"""
import time
import board
import pwmio
import supervisor
from adafruit_motor import servo



# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)

def fire():
    for angle in range(0, 180, -50):                                          
        my_servo.angle = angle
        time.sleep(0.01)
    for angle in range(180, 0, -5):
        my_servo.angle = angle
        time.sleep(0.05)

while True:

    for angle in range(0, 180, -50):                                          
        my_servo.angle = angle
        time.sleep(0.01)
    for angle in range(180, 0, -5):
        my_servo.angle = angle
        time.sleep(0.05)
