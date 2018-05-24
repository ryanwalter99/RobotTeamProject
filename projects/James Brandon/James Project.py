#main graphical interface look at m5 (pc)
#  code for pc and robots two files
# tkinter for more complex canvas and drawing (more examples)
#ev3 side, loop
#both sides create mqqt
#put stuff in robot controller
#ev3 def follow line(robot,
#(pc) make own delegate not robot and delegate has robot as instance variable def....self.robot.method
#pc
#def main
#   mqqt
#   mqqt.sendmessage
#   ...complicate
#ev3.1
#   def main()
#   d = Delegate
#   class Delegate(object)
#   def init()
#       self.robot.... =snatcher
#   self.complicated(self)


#ev3.2(no pc interaction)
#   def main()
#       robot
#       button = ev3.button()
#       button.on_up = la....foo(robot,..)
#       def foo(robot,....)
#

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import time
import ev3dev.ev3 as ev3
import math
import robot_controller as robo
COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
# robot = robo.Snatch3r()

def main():
    # : 2. Setup an mqtt_client.  Notice that since you don't need to receive any messages you do NOT need to have
    # a MyDelegate class.  Simply construct the MqttClient with no parameter in the constructor (easy).

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Rescue Bot")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=10)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=10, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: send_forward(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: send_forward(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: send_left(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: send_left(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: send_stop(mqtt_client)
    root.bind('<space>', lambda event: send_stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: send_right(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Right>', lambda event: send_right(mqtt_client, left_speed_entry, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: send_back(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: send_back(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    rescue_button = ttk.Button(main_frame, text="Rescue")
    rescue_button.grid(row=6, column=1)
    rescue_button['command'] = (lambda: rescue(mqtt_client))

    root.mainloop()
    #search_and_rescue()

# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
# : 4. Implement the functions for the drive button callbacks.

# : 5. Call over a TA or instructor to sign your team's checkoff sheet and do a code review.  This is the final one!
#
# Observations you should make, you did basically this same program using the IR Remote, but your computer can be a
# remote control that can do A LOT more than an IR Remote.  We are just doing the basics here.


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")

def send_forward(mqtt_client, left_speed_entry, right_speed_entry):
    print("forward")
    mqtt_client.send_message("drive",[int(left_speed_entry.get()),
                                      int(right_speed_entry.get())])

def send_left(mqtt_client, left_speed_entry, right_speed_entry):
    print("left")
    mqtt_client.send_message("drive",[-int(left_speed_entry.get()),
                                      int(right_speed_entry.get())])

def send_right(mqtt_client, left_speed_entry, right_speed_entry):
    print("right")
    mqtt_client.send_message("drive",[int(left_speed_entry.get()),
                                      -int(right_speed_entry.get())])

def send_back(mqtt_client,left_speed_entry,right_speed_entry):
    print("backward")
    mqtt_client.send_message("backward",[int(left_speed_entry.get()),
                                         int(right_speed_entry.get())])

def send_stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()

def search_and_rescue():
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
    color_sensor = ev3.ColorSensor(ev3.INPUT_1)
    while True:
        if color_sensor.color == 2:
            print('Blue is Safe')
            left_motor.stop()
            right_motor.stop()
            time.sleep(1)
            break

        if color_sensor.color == 3:
            print("Green is Safe")
            left_motor.stop()
            right_motor.stop()
            time.sleep(1)
            break

        if color_sensor.color == 5:
            print("Red Needs Help!!")
            ev3.Sound.speak('Help is Here!').wait()
            left_motor.stop()
            right_motor.stop()
            time.sleep(1)
            break

def rescue(self):
        forward_speed = 300
        turn_speed = 100
        while not self.touch_sensor.is_pressed:
            current_heading = self.beacon_seeker.heading
            current_distance = self.beacon_seeker.distance
            if current_distance == -128:
                print("Victim remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    print("Needed on the right, heading distance: ", current_distance)
                    if current_distance == 0:
                        self.stop()
                        return True
                    if current_distance > 0:
                        self.drive(forward_speed, forward_speed)
                if math.fabs(current_heading) > 2 and math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        self.drive(-turn_speed, turn_speed)
                    if current_heading > 0:
                        self.drive(turn_speed, -turn_speed)
                if math.fabs(current_heading) > 10:
                    self.drive(-forward_speed, forward_speed)
            time.sleep(0.2)
        print("Call For Back up!")
        self.stop()
        return False


    # def Search(mqtt_client):
    # mqtt_client.send_message("search1")
    #
    #
    # def Rescue(mqtt_client):
    # mqtt_client.send_message("currentcolor")
main()

