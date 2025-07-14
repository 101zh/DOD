import select
import time
import board
import pwmio
import sys
import gc
from adafruit_motor import servo

can_shoot : bool = False

class DOD_servo:
    def __init__(self, pin, duty_cycle: int, frequency: int):
        self = self
        self.servo = servo.Servo(pwmio.PWMOut(
            pin, duty_cycle=duty_cycle, frequency=frequency))
        self.current_angle = 90
        self.target_angle = 90
        self.running_to_target = False

    def set_target_angle(self, angle_serial_input):
        if self.running_to_target:
            return
        
        print(angle_serial_input)
        new_target = ""

        for char in angle_serial_input:
            new_target += char

        print(new_target)
        self.target_angle = float(new_target)

    def run_to_target_angle(self):
            self.running_to_target = True
            if self.current_angle < self.target_angle:
                # 0 - 180 degrees, 5 degrees at a time.
                for angle in range(self.current_angle, self.target_angle, 1):
                    self.servo.angle = angle
                    self.current_angle = angle
                    time.sleep(0.01)
            elif self.current_angle > self.target_angle:
                # 180 - 0 degrees, 5 degrees at a time.
                for angle in range(self.current_angle, self.target_angle, -1):
                    self.servo.angle = angle
                    self.current_angle = angle
                    time.sleep(0.01)

            self.running_to_target = False

    def run_to_target_angle_fast(self):
        self.servo.angle = self.target_angle

base_servo : DOD_servo = DOD_servo(board.GP0, 2**15, 50)
trigger_servo : DOD_servo = DOD_servo(board.GP1, 2**15, 50)

buffered_input = []

def read_serial_input():
    select_result = select.select([sys.stdin], [], [], 0)
    while select_result[0]:
        input_character = sys.stdin.read(1)
        print(f"Received: {repr(input_character)}")

        if (input_character == "\n"):
            print(buffered_input)
            determine_action(buffered_input)
            buffered_input.clear()
        else:
            buffered_input.append(input_character)

        select_result = select.select([sys.stdin], [], [], 0)

def remove_tags(serial_input: list):
    serial_input.pop(0)
    serial_input.pop(0)

def determine_action(serial_input: list):
    global can_shoot

    tag: str = serial_input[0] + serial_input[1]
    remove_tags(serial_input)

    if (tag == "~b"):
        base_servo.set_target_angle(serial_input)
    elif(tag == "~s"):
        shoot()
    elif(tag == "~r"):
        trigger_servo.set_target_angle(serial_input)

def shoot():
    trigger_servo.set_target_angle(["1","3","5"])
    trigger_servo.run_to_target_angle_fast()
    time.sleep(1)
    trigger_servo.set_target_angle(["8","9"])
    trigger_servo.run_to_target_angle_fast()
    time.sleep(1)

while True:
    base_servo.run_to_target_angle()
    trigger_servo.run_to_target_angle()
    read_serial_input()
