from PiicoDev_VL53L1X import PiicoDev_VL53L1X
import time

distSensor = PiicoDev_VL53L1X()

# Function to start the timer
def start_timer():
    return time.time()

# Function to stop the timer
def stop_timer(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

# Function to format and print the current lap time
def print_lap_time(lap_start_time):
    if lap_start_time is not None:
        elapsed_time = time.time() - lap_start_time
        minutes = int(elapsed_time / 60)
        seconds = int(elapsed_time % 60)
        hundredths = int((elapsed_time - int(elapsed_time)) * 100)
        print(f"Current Lap Time: {minutes:02d}:{seconds:02d}:{hundredths:02d} seconds")

# Initialize variables
timer_running = False
start_time = 0
lap_start_time = None  # Initialize lap_start_time

# Function to clear the value of dist
def clear_dist():
    global dist  # make the dist variable global
    dist = 0

try:
    while True:
        dist = distSensor.read()  # read the distance in millimeters

        if 0 < dist < 300 and not timer_running:
            start_time = start_timer()
            lap_start_time = start_time  # Record lap start time
            timer_running = True
            print("Lap Start.")
            print("*" * 20)
            time.sleep(1)
            clear_dist()

        if 0 < dist < 300 and timer_running:
            elapsed_time = stop_timer(start_time)
            timer_running = False
            print(f"Lap Time: {elapsed_time:.2f} seconds")
            print("*" * 20)
            clear_dist()

        print_lap_time(lap_start_time)  # Print current lap time

except KeyboardInterrupt:
    print("Time Killed")
#9:20 12/10/2023