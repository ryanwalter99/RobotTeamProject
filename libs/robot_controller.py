"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)


        assert self.left_motor.connected
        assert self.right_motor.connected

    def drive_inches(self,inches,speed,stop_action='coast'):

        new_speed = (4.6 / 400) * (speed)
        ## 16.67 is degrees the wheels move in one inch
        degrees = (speed) * (inches / new_speed)


        self.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed , stop_action=stop_action)
        self.right_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed , stop_action=stop_action)

        time.sleep(inches / new_speed)

        self.left_motor.stop()
        self.right_motor.stop()

    def drive_inches_backward(self,inches,speed,stop_action='coast'):
        self.drive_inches(-1*inches,-1*speed,stop_action=stop_action)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """
        turn_degrees is made to take input on degrees to turn. It moves the motors in opposite directions depending on
        if the input is positive or negative. The function will beep when it has finished.
        """
        degrees_per_turning_degree = 4
        degrees_per_wheel = degrees_to_turn * degrees_per_turning_degree
        if turn_speed_sp < 0:
            self.left_motor.run_to_rel_pos(position_sp=degrees_per_wheel, speed_sp=turn_speed_sp)
            self.right_motor.run_to_rel_pos(position_sp=-degrees_per_wheel, speed_sp=turn_speed_sp)
        if turn_speed_sp > 0:
            self.left_motor.run_to_rel_pos(position_sp=-degrees_per_wheel, speed_sp=turn_speed_sp)
            self.right_motor.run_to_rel_pos(position_sp=degrees_per_wheel, speed_sp=turn_speed_sp)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def loop_forever(self):
        self.running = True
        while self.running:
            if self.ir_sensor.proximity < 20:
                ev3.Sound.beep()
                self.stop()
                ev3.Sound.speak('You went in the hole. You win.')
            elif self.color_sensor.color == ev3.ColorSensor.COLOR_BLUE:
                self.stop()
                ev3.Sound.speak('You went in the water. You lose.')
            time.sleep(0.1)




