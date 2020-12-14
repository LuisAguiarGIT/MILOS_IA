#!/usr/bin/env python3

from time   import sleep
from random import choice, randint

from ev3dev2.motor import OUTPUT_D, OUTPUT_C, LargeMotor
from ev3dev2.sensor.lego import InfraredSensor, TouchSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

# Connect two large motors on output ports B and C:
motors = [LargeMotor(address) for address in (OUTPUT_D, OUTPUT_C)]

# Connect infrared and touch sensors.
ir = InfraredSensor()
ts = TouchSensor()

print('Robot Starting')

# We will need to check EV3 buttons state.
btn = Button()

def start():
    """
    Start both motors. `run-direct` command will allow to vary motor
    performance on the fly by adjusting `duty_cycle_sp` attribute.
    """
    for m in motors:
        m.run_direct()

def backup():
    """
    Back away from an obstacle.
    """

    # Sound backup alarm.
    spkr = Sound()
    spkr.tone([(1000, 500, 500)] * 3)

    # Turn backup lights on:
    leds = Leds()

    for light in ('LEFT', 'RIGHT'):
        leds.set_color(light, 'RED')

    # Stop both motors and reverse for 1.5 seconds.
    # `run-timed` command will return immediately, so we will have to wait
    # until both motors are stopped before continuing.
    for m in motors:
        m.stop(stop_action='brake')
        m.run_timed(speed_sp=-500, time_sp=1500)

    # When motor is stopped, its `state` attribute returns empty list.
    # Wait until both motors are stopped:
    while any(m.state for m in motors):
        sleep(0.1)

    # Turn backup lights off:
    for light in ('LEFT', 'RIGHT'):
        leds.set_color(light, 'GREEN')


def turn():
    """
    Turn the robot in random direction.
    """

    # We want to turn the robot wheels in opposite directions from 1/4 to 3/4
    # of a second. Use `random.choice()` to decide which wheel will turn which
    # way.
    power = choice([(1, -1), (-1, 1)])
    t = randint(250, 750)

    for m, p in zip(motors, power):
        m.run_timed(speed_sp = p * 750, time_sp = t)

    # Wait until both motors are stopped:
    while any(m.state for m in motors):
        sleep(0.1)

# Run the robot until a button is pressed.
start()
while not btn.any():

    if ts.is_pressed:
        # We bumped an obstacle.
        # Back away, turn and go in other direction.
        backup()
        turn()
        start()

    # Infrared sensor in proximity mode will measure distance to the closest
    # object in front of it.
    distance = ir.proximity

    if distance > 60:
        # Path is clear, run at full speed.
        dc = 95
    else:
        # Obstacle ahead, slow down.
        dc = 30

    for m in motors:
        m.duty_cycle_sp = dc

    sleep(0.1)

# Stop the motors before exiting.
for m in motors:
    m.stop()