"""
Functions for TURNING the robot LEFT and RIGHT.
Authors: David Fisher, David Mutchler and Alex Gipson.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

# TODO: 2. Implment turn_left_seconds, then the relevant part of the test function.
#          Test and correct as needed.
#   Then repeat for turn_left_by_time.
#   Then repeat for turn_left_by_encoders.
#   Then repeat for the turn_right functions.

import ev3dev.ev3 as ev3
import time


def test_turn_left_turn_right():
    """
    Tests the turn_left and turn_right functions, as follows:
      1. Repeatedly:
          -- Prompts for and gets input from the console for:
             -- Seconds to travel
                  -- If this is 0, BREAK out of the loop.
             -- Speed at which to travel (-100 to 100)
             -- Stop action ("brake", "coast" or "hold")
          -- Makes the robot run per the above.
      2. Same as #1, but gets degrees and runs turn_left_by_time.
      3. Same as #2, but runs turn_left_by_encoders.
      4. Same as #1, 2, 3, but tests the turn_right functions.
    """


    speed = int(input('speed between -100 to 100'))
    stoping_action = input('type brake, coast, or hold')

    while True:
        x = int(input('insert time'))
        if x == 0:
            break
        turn_left_seconds(x, speed, stoping_action)

    while True:
        y = int(input('insert degrees'))
        if y == 0:
            break
        turn_left_by_time(y, speed, stoping_action)

    while True:
        y = int(input('insert degrees'))
        if y == 0:
            break
        turn_left_by_encoders(y, speed, stoping_action)


    while True:
        x = int(input('insert time'))
        if x == 0:
            break
        turn_right_seconds(x, speed, stoping_action)

    while True:
        y = int(input('insert degrees'))
        if y == 0:
            break
        turn_right_by_time(y, speed, stoping_action)

    while True:
        y = int(input('insert degrees'))
        if y == 0:
            break
        turn_right_by_encoders(y, speed, stoping_action)


def turn_left_seconds(seconds, speed, stop_action):
    """
    Makes the robot turn in place left for the given number of seconds at the given speed,
    where speed is between -100 (full speed turn_right) and 100 (full speed turn_left).
    Uses the given stop_action.
    """

    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected
    print(speed, seconds, stop_action)
    print(type(speed))
    print(type(seconds))
    print(type(stop_action))
    right_motor.run_timed(speed_sp=speed * 8, time_sp=seconds * 1000, stop_action=stop_action)
    left_motor.run_timed(speed_sp=-speed * 8, time_sp=seconds * 1000, stop_action=stop_action)
    right_motor.wait_while('running')
    left_motor.wait_while('running')


def turn_left_by_time(degrees, speed, stop_action):
    """
    Makes the robot turn in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed turn_right) and 100 (full speed turn_left).
    Uses the algorithm:
      0. Compute the number of seconds to move to achieve the desired distance.
      1. Start moving.
      2. Sleep for the computed number of seconds.
      3. Stop moving.
    """
# Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected
    seconds = (int(input('how many seconds?')))

    right_motor.run_timed(speed_sp=speed * 8, time_sp=seconds * 1000, poistion_sp=degrees, stop_action=stop_action)
    left_motor.run_timed(speed_sp=-speed * 8, time_sp=seconds * 1000, position_sp=degrees, stop_action=stop_action)
    right_motor.wait_while('running')
    left_motor.wait_while('running')


def turn_left_by_encoders(degrees, speed, stop_action):
    """
    Makes the robot turn in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed turn_right) and 100 (full speed turn_left).
    Uses the algorithm:
      1. Compute the number of degrees the wheels should turn to achieve the desired distance.
      2. Move until the computed number of degrees is reached.
    """
# Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected
    seconds = int(input('how many seconds'))

    right_motor.run_timed(speed_sp=speed * 8, time_sp=seconds * 1000, position_sp=degrees, stop_action=stop_action)
    left_motor.run_timed(speed_sp=-speed * 8, time_sp=seconds * 1000, position_sp=-degrees, stop_action=stop_action)
    right_motor.wait_while('running')
    left_motor.wait_while('running')

def turn_right_seconds(seconds, speed, stop_action):
    """ Calls turn_left_seconds with negative speeds to achieve turn_right motion. """

# Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    left_motor.run_timed(speed_sp=speed, time_sp=seconds * 1000, stop_action=stop_action)
    right_motor.run_timed(speed_sp=-speed, time_sp=seconds * 1000, stop_action=stop_action)
    right_motor.wait_while('running')
    left_motor.wait_while('running')

def turn_right_by_time(degrees, speed, stop_action):
    """ Calls turn_left_by_time with negative speeds to achieve turn_right motion. """

# Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected
    seconds = int(input('how many seconds'))

    right_motor.run_timed(speed_sp=-speed * 8, time_sp=seconds * 1000, position_sp=-degrees, stop_action=stop_action)
    left_motor.run_timed(speed_sp=speed * 8, time_sp=seconds * 1000, position_sp=degrees, stop_action=stop_action)
    right_motor.wait_while('running')
    left_motor.wait_while('running')

def turn_right_by_encoders(degrees, speed, stop_action):
    """ Calls turn_left_by_encoders with negative speeds to achieve turn_right motion. """

# Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected
    seconds = int(input('how many seconds'))

    right_motor.run_timed(speed_sp=-speed * 8, time_sp=seconds*1000, position_sp=-degrees, stop_action=stop_action)
    left_motor.run_timed(speed_sp=speed * 8, time_sp=seconds*1000, position_sp=degrees, stop_action=stop_action)
    right_motor.wait_while('running')
    left_motor.wait_while('running')

test_turn_left_turn_right()