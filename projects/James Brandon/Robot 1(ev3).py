import mqtt_remote_method_calls as com
import robot_controller as robo
import time
import ev3dev.ev3 as ev3

# def main(self):
#     class Delegate(object):
#         def __init__(self):
#             self.robot = robo.Snatch3r()
#
#     mqtt_client = com.MqttClient()
#     mqtt_client.connect_to_pc()
#     self.robot.loop_forever()
def main():
    robot = RescueBot()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()


class RescueBot(object):

    def __init__(self):
        self.running = True
        self.robot = robo.Snatch3r()
        self.btn = ev3.Button()
        # self.btn.on_up = lambda state: self.drive_to_color(state, ev3.ColorSensor.COLOR_RED)
        # self.btn.on_down = lambda state: self.drive_to_color(state,  ev3.ColorSensor.COLOR_BLUE)
        # self.btn.on_left = lambda state: self.drive_to_color(state,  ev3.ColorSensor.COLOR_BLACK)
        # self.btn.on_right = lambda state: self.drive_to_color(state,  ev3.ColorSensor.COLOR_WHITE)
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor(ev3.INPUT_4)
        self.beacon_seeker = ev3.BeaconSeeker(channel=4)
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.max_speed = 900

        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.color_sensor
        assert self.pixy
        ##self.btn.on_backspace = lambda state: handle_shutdown(state, dc)

    def listining(self):
        while True:
            self.btn.process()
            time.sleep(.05)

    def stop(self):
        self.right_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')

    def drive(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def backward(self, left_speed_entry, right_speed_entry):
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def arm_up(self):
        """
        arm_up is made to raise the arm up when the desired button is pressed. This function will always raise the
        arm as fast as possible and will beep when it is fully raised.
        """
        self.arm_motor.run_forever(speed_sp=self.max_speed)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        self.arm_motor.stop()
        ev3.Sound.beep().wait()

    def arm_down(self):
        """
        arm_down is made to lower the arm down when the desired button is pressed. This function will always lower the
        arm as fast as possible and will beep when it is fully lowered.
        """
        print('Hi')

        self.arm_motor.run_to_rel_pos(position_sp=-1*14.2*360, speed_sp=self.max_speed)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()


    def shutdown(self):
        """
        shutdown is made to stop all movement of the robot and finish running code when the desired button is pressed.
        This function changes the LEDs to Green and says 'Goodbye' before after everything is stopped.
        """
        self.arm_motor.stop()
        self.left_motor.stop()
        self.right_motor.stop()
        print('Goodbye!')
        ev3.Sound.speak("Goodbye").wait()

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

main()


