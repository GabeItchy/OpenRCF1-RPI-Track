import pygame
import RPi.GPIO as GPIO
# import requests
# import socket

"""""""""
# Relays server position to pi 4 server
# TODO: Start Pi 4 server and add server information
# IP and port of the Raspberry Pi 4 server
server_ip = 'your_pi_4_ip_address'
server_port = 5000

# Function to send servo position data to the server
def send_servo_position(position):
    data = {"servo_position": position}
    try:
        response = requests.post(f'http://{server_ip}:{server_port}/update_servo', json=data)
        if response.status_code == 200:
            print("Servo position sent successfully")
        else:
            print("Error sending servo position")
    except Exception as e:
        print(f"Error: {e}")
"""""""""
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

    # Define the index for the right trigger axis (may vary on different controllers)
    RIGHT_TRIGGER_AXIS = 5  # This index is based on typical PS4 controller configuration

    # Define the index for the left trigger axis (may vary on different controllers)
    LEFT_TRIGGER_AXIS = 2  # This index is based on typical PS4 controller configuration

    # Define the PWM pin (GPIO 18)
    PWM_PIN = 18  # Change this to your desired GPIO pin (e.g., GPIO18)

    # Set up PWM on the selected pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PWM_PIN, GPIO.OUT)

    # Create a PWM instance with a frequency of 1000 Hz
    pwm = GPIO.PWM(PWM_PIN, 1000)
    pwm.start(0)  # Start with a duty cycle of 0%

    try:
        while True:
            pygame.event.pump()

            # Get the value of the right trigger axis (0.0 when not pressed, 1.0 when fully pressed)
            right_trigger_value = joystick.get_axis(RIGHT_TRIGGER_AXIS)

            # Map the right trigger value to a PWM duty cycle (0% to 100%)
            right_duty_cycle = (right_trigger_value + 1.0) * 50.0  # Scale to the 0-100 range
            right_duty_cycle = max(0.0, min(100.0, right_duty_cycle))

            # Get the value of the left trigger axis (0.0 when not pressed, 1.0 when fully pressed)
            left_trigger_value = joystick.get_axis(LEFT_TRIGGER_AXIS)

            # Map the left trigger value to a PWM duty cycle (0% to -100%)
            left_duty_cycle = (-left_trigger_value + 1.0) * 50.0  # Scale to the 0-100 range with negative values
            left_duty_cycle = max(-100.0, min(100.0, left_duty_cycle))

            # Update the PWM duty cycle
            combined_duty_cycle = right_duty_cycle + left_duty_cycle
            combined_duty_cycle = max(0.0, min(100.0, combined_duty_cycle))
            pwm.ChangeDutyCycle(combined_duty_cycle)

            # Print the trigger values in the shell
            print(f"Right Trigger Value: {right_trigger_value:.2f}, Left Trigger Value: {left_trigger_value:.2f}")
    
    except KeyboardInterrupt:
        # Clean up and exit when Ctrl+C is pressed
        pwm.stop()
        GPIO.cleanup()
