import pygame
import pigpio
import time  
import requests

# Initialize Pygame
pygame.init()

# Initialize the joystick subsystem
pygame.joystick.init()

# Check if any joystick (including the PS4 controller) is connected
if pygame.joystick.get_count() == 0:
    print("No joystick found. Make sure your PS4 controller is connected.")
else:
    # Initialize the first joystick (change index if you have multiple controllers)
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Define the index for the PS4 controller's left joystick's X-axis
    LEFT_JOYSTICK_X_AXIS = 0  # This index may vary on different controllers

    # Define the PWM pin for controlling the servo (GPIO 12)
    SERVO_PIN = 12  # Change this to GPIO 12

    # Create a pigpio instance
    pi = pigpio.pi()

    # Define servo position limits
    MIN_SERVO_POSITION = 700
    MAX_SERVO_POSITION = 2000

    # Set a lower PWM frequency (e.g., 50 Hz for smoother motion)
    pi.set_PWM_frequency(SERVO_PIN, 50)

    try:
        while True:
            pygame.event.pump()

            # Get the value of the left joystick's X-axis (-1.0 to 1.0, 0.0 is centered)
            left_joystick_x = joystick.get_axis(LEFT_JOYSTICK_X_AXIS)

            # Invert the joystick value
            inverted_joystick_x = -left_joystick_x

            # Map the inverted joystick value to servo position
            servo_position = int(
                (inverted_joystick_x + 1) * (MAX_SERVO_POSITION - MIN_SERVO_POSITION) / 2 + MIN_SERVO_POSITION
            )

            # Ensure the servo position is within the valid range
            servo_position = max(MIN_SERVO_POSITION, min(MAX_SERVO_POSITION, servo_position))

            # Set the servo position
            pi.set_servo_pulsewidth(SERVO_PIN, servo_position)

            # Print the servo position
            print(f"Servo Position: {servo_position} microseconds")

            # Check if the joystick is at rest (close to zero)
            if abs(inverted_joystick_x) < 0.1:
                # Return the servo to the middle point (position 1700)
                pi.set_servo_pulsewidth(SERVO_PIN, 1300)

            # Add a small sleep interval (e.g., 0.01 seconds) for smoother PWM signal
            time.sleep(0.01)

    except KeyboardInterrupt:
        # Clean up and exit when Ctrl+C is pressed
        pi.set_servo_pulsewidth(SERVO_PIN, 0)  # Stop the servo
        pi.stop()
