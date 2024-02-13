import time
import pigpio
from evdev import InputDevice, categorize, ecodes

# Initialize pigpio and set up PWM on GPIO pin 15
pi = pigpio.pi()
if not pi.connected:
    exit(1)

pi.set_mode(15, pigpio.OUTPUT)
pi.set_PWM_frequency(15, 50)  # Change the pin number here to 15

# Set up PWM duty cycle
min_duty = 3
max_duty = 100
current_duty = 0

# Find the event device for your DualShock 4 controller
controller = InputDevice("/dev/input/event2")  # Replace "X" with the correct event number

try:
    while True:
        event = controller.read_one()
        if event is not None:
            if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_RZ:
                trigger_value = event.value / 255.0  # Scale trigger input from 0 to 1
                duty_cycle = min(max_duty, max(min_duty, trigger_value * (max_duty - min_duty) + min_duty))
                pi.set_PWM_dutycycle(15, duty_cycle)
                print(f"Trigger Value: {trigger_value:.2f}, Duty Cycle: {duty_cycle:.2f}")

                if trigger_value == 0:
                    # Set duty cycle to 0 immediately when trigger is released
                    pi.set_PWM_dutycycle(15, 0)
                    print("Trigger Value is 0, setting Duty Cycle to 0")

        time.sleep(0.01)  # Sleep to conserve resources
        
except KeyboardInterrupt:
    pass
finally:
    pi.set_PWM_dutycycle(15, 0)  # Ensure PWM is off
    pi.stop()

