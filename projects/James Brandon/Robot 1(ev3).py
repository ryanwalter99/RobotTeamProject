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


main()


