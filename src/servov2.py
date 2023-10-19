import pigpio
import pygame
import time
import socket
from flask import Flask, request, jsonify    

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

# Initialize Flask app
app = Flask(__name)

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

# API route to update servo position
@app.route('/update_servo', methods=['POST'])
def update_servo():
    data = request.get_json()
    servo_position = data.get("servo_position")
    
    # Update the servo position locally
    pi.set_servo_pulsewidth(servo_gpio_pin, servo_position)
    
    return "Servo position updated", 200

# Function to periodically send servo position to the server
def send_servo_position_periodically():
    while True:
        send_servo_position(pi.get_servo_pulsewidth(servo_gpio_pin))
        time.sleep(1)

if __name__ == '__main__':
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': server_port})
    flask_thread.daemon = True
    flask_thread.start()

    # Start the servo update thread
    servo_update_thread = threading.Thread(target=send_servo_position_periodically)
    servo_update_thread.daemon = True
    servo_update_thread.start()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:  # Left joystick X-axis
                        # Map the joystick input (-1 to 1) to servo pulse width and flip the direction
                        joystick_value = event.value
                        pulse_width = int(servo_center - joystick_value * servo_range / 2)
                        pi.set_servo_pulsewidth(servo_gpio_pin, pulse_width)
                
                time.sleep(0.01)

    except KeyboardInterrupt:
        pass

    # Clean up and exit
    joystick.quit()
    pi.set_servo_pulsewidth(servo_gpio_pin, 0)  # Turn off the servo
    pi.stop()
