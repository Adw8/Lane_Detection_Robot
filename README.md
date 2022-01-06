# Lane_Detection_Robot

This is a robot that detects and stays between two lanes of a road, it achieves this using Computer Vision. This project was made using the OpenCV library of Python, Raspberri Pi (4b) and Arduino Uno. It uses two DC motor controlled wheels in the back and one sliding wheel in the front in order to achieve maximum efficiency with minimum resources.
It also uses a motor driver (L293D) in order to control the dc motored wheels. The Raspberry Pi has a camera attached to it that takes in input of the road, processes it, detects the lane and calculates the steering angle for robot to move.

It sends this value to the Arduino, to which it is connected using I2C protocol, and the Arduino makes the robot move based on the steering angle, using an algorithm that calculated speed and direction of the robot.

All of this is achieved in real time.

