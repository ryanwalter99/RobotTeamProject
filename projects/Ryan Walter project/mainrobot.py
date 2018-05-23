import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

class Drawer(object):
    """ Helper class that might be useful to communicate between different callbacks."""


    def __init__(self):
        self.running = True
        self.robot = robo.Snatch3r()
        self.btn = ev3.Button()
        self.btn.on_up = lambda state: self.drive_to_color(state, ev3.ColorSensor.COLOR_RED)
        self.btn.on_down = lambda state: self.drive_to_color(state,  ev3.ColorSensor.COLOR_BLUE)
        self.btn.on_left = lambda state: self.drive_to_color(state,  ev3.ColorSensor.COLOR_BLACK)
        self.btn.on_right = lambda state: self.drive_to_color(state,  ev3.ColorSensor.COLOR_WHITE)
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


    def drive_to_color(self,button_state, color_to_seek):
        COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
        if button_state:
            ev3.Sound.speak("Seeking " + COLOR_NAMES[color_to_seek]).wait()

            self.robot.drive(200, 200)
            while True:
                if self.robot.color_sensor.color == color_to_seek:
                    self.robot.stop()
                    ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()
                    time.sleep(.01)
                    break

    def color_to_seek(self):

        print("--------------------------------------------")
        print(" Drive to the color")
        print("  Up button goes to Red")
        print("  Down button goes to Blue")
        print("  Left button goes to Black")
        print("  Right button goes to White")
        print("--------------------------------------------")

        print("Press Back to exit this program.")



        # For our standard shutdown button.

        # DONE: 2. Uncomment the lines below to setup event handlers for these buttons.


        # while dc.running:
        #     btn.process()
        #     time.sleep(0.01)

        print("Starting!")
        ev3.Sound.speak("Seeking color").wait()


def main():
    dc = Drawer()

    mqtt_client = com.MqttClient(dc)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker


    dc.listining()









def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


main()
