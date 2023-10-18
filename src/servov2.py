import pigpio
import pygame
import time

# Servo Configuration
servo_gpio_pin = 12
servo_min_pulse_width = 1555  # Minimum pulse width for the servo (in microseconds)
servo_max_pulse_width = 2500  # Maximum pulse width for the servo (in microseconds)
servo_range = servo_max_pulse_width - servo_min_pulse_width
servo_center = (servo_max_pulse_width + servo_min_pulse_width) // 2  # Center position

# Initialize pigpio
pi = pigpio.pi()

# Initialize pygame
pygame.init()
pygame.joystick.init()

# Connect to the first joystick (index 0)
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Debugging function to print servo position
# def print_servo_position(pulse_width):
    # print(f"Servo Position: {pulse_width} (Microseconds)")

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:  # Left joystick X-axis
                    # Map the joystick input (-1 to 1) to servo pulse width and flip the direction
                    joystick_value = event.value
                    pulse_width = int(servo_center - joystick_value * servo_range / 2)
                    pi.set_servo_pulsewidth(servo_gpio_pin, pulse_width)
                    # print_servo_position(pulse_width)

        time.sleep(0.01)

except KeyboardInterrupt:
    pass

# Clean up and exit
joystick.quit()
pi.set_servo_pulsewidth(servo_gpio_pin, 0)  # Turn off the servo
pi.stop()
