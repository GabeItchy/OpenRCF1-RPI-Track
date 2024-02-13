from turtle import left
import pygame
import pigpio
import time

# Initialize pygame
pygame.init()
pygame.joystick.init()

# Initialize pigpio
pi = pigpio.pi()

# Set GPIO pins for servos
steering = 23 
throttlebox = 18  

# Setup joysticks
joystick_left = pygame.joystick.Joystick(0)
joystick_left.init()

joystick_right = pygame.joystick.Joystick(0)
joystick_right.init()

# Define servo limits
servo_min_left = 0    # Updated minimum angle (in degrees)
servo_max_left = 200  # Updated maximum angle (in degrees)

servo_min_right = 80   # Minimum angle (in degrees)
servo_max_right = 120  # Maximum angle (in degrees)

# Map joystick values to servo angles
def map_values(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

try:
    while True:
        pygame.event.get()

        # Steering Code using joystick
        x_value_left = -joystick_left.get_axis(0)

        mapped_angle_left = int(map_values(x_value_left, -1, 1, servo_min_left, servo_max_left))
        mapped_angle_left = max(servo_min_left, min(mapped_angle_left, servo_max_left))
        pi.set_servo_pulsewidth(steering, mapped_angle_left * 1000 / 180 + 1000)

        # Throttle box using right trigger
        trigger_value_right = joystick_right.get_axis(5)
        mapped_angle_right = int(map_values(trigger_value_right, -1, 1, servo_min_right, servo_max_right))
        mapped_angle_right = max(servo_min_right, min(mapped_angle_right, servo_max_right))
        pi.set_servo_pulsewidth(throttlebox, mapped_angle_right * 1000 / 180 + 1000)

        # Optional: Adjust the delay if needed
        time.sleep(0.05)

except KeyboardInterrupt:
    pi.set_servo_pulsewidth(steering, 0)
    pi.set_servo_pulsewidth(throttlebox, 0)
    pi.stop()
    pygame.quit()
