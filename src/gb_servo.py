import pygame
import pigpio
import time

# Initialize pygame and the controller
pygame.init()
pygame.joystick.init()

# Connect to the pigpio daemon
pi = pigpio.pi()

# Initialize the servo GPIO pin (change this to your GPIO pin)
servo_gpio_pin = 12
pi.set_mode(servo_gpio_pin, pigpio.OUTPUT)

# Configure the servo parameters (pulsewidth range for your servo)
servo_min = 1000  # Minimum pulsewidth (Far Left)
servo_middle = 1500  # Middle pulsewidth (Middle)
servo_max = 2000  # Maximum pulsewidth (Far Right)

# Initialize the controller
joystick = pygame.joystick.Joystick(0)
joystick.init()

current_position = servo_middle  # Start in the Middle position

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 2:  # Triangle button pressed (Upshifting)
                    # Upshift to the next position
                    if current_position == servo_middle:
                        current_position = servo_min  # Upshift from Neutral to gear_1
                    elif current_position == servo_min:
                        current_position = servo_max  # Upshift from gear_1 to gear_2

                elif event.button == 0:  # X button pressed (Downshifting)
                    # Downshift to the next position
                    if current_position == servo_max:
                        current_position = servo_min  # Downshift to gear_1 from gear_2 
                    elif current_position == servo_min:
                        current_position = servo_middle  # Downshift to neutral from gear_1

                # Set the servo position
                pi.set_servo_pulsewidth(servo_gpio_pin, current_position)

        print(f"Current Gear Position: {'gear_1' if current_position == servo_min else ('gear_n' if current_position == servo_middle else 'gear_2')}")
        time.sleep(0.01)  # Add a small delay to avoid excessive updates

except KeyboardInterrupt:
    pass

# Clean up
pi.set_servo_pulsewidth(servo_gpio_pin, 0)
pi.stop()
pygame.quit()
