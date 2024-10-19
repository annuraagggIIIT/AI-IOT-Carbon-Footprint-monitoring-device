import serial
import time
import json
import re
from datetime import datetime

# Open serial port
try:
    ser = serial.Serial('COM3', 115200)
    print("Serial connection established.")
except serial.SerialException as e:
    print(f"Error opening serial connection: {e}")
    ser = None

# Pattern to match all gas data
pattern = re.compile(
    r'MQ-2 Data: LPG: ([\d\.]+) ppm, Smoke: ([\d\.]+) ppm|'
    r'MQ-3 Data: Alcohol: ([\d\.]+) ppm|'
    r'MQ-5 Data: LPG: ([\d\.]+) ppm, Methane: ([\d\.]+) ppm|'
    r'MQ-9 Data: CO: ([\d\.]+) ppm, Flammable Gases: ([\d\.]+) ppm'
)

# Buffer to hold sensor data
sensor_buffer = {
    "lpg": None,
    "smoke": None,
    "alcohol": None,
    "methane": None,
    "co": None,
    "flammable_gas": None,
    "timestamp": None
}

# Flags to track whether each sensor's data has been captured
data_flags = {
    "mq2": False,
    "mq3": False,
    "mq5": False,
    "mq9": False
}

start_time = time.time()
timeout_duration = 10  

def write_to_json(data):
    """Write sensor data to gas.json with timestamp."""
    print("Attempting to write data to gas.json...")

    try:
        with open('gas.json', 'r') as file:
            existing_data = json.load(file)
            print("Existing data loaded from gas.json.")
    except FileNotFoundError:
        print("gas.json not found. Creating a new file.")
        existing_data = []
    except json.JSONDecodeError:
        print("Error decoding gas.json. Creating a new file with valid JSON.")
        existing_data = []

    if data:
        print(f"Data to write to gas.json: {data}")
        existing_data.append(data)

        try:
            # Write to gas.json (with timestamp)
            with open('gas.json', 'w') as file:
                json.dump(existing_data, file, indent=4)
                print("Data successfully written to gas.json")
        except Exception as e:
            print(f"Error writing to gas.json: {e}")
    else:
        print("No valid data to write to gas.json.")

def process_data(raw_data):
    """Process raw sensor data, update buffer, and check if all data is ready."""
    global sensor_buffer, data_flags

    match = pattern.search(raw_data)
    if match:
        if match.group(1) and match.group(2):  # MQ-2: LPG and Smoke
            sensor_buffer["lpg"] = float(match.group(1))
            sensor_buffer["smoke"] = float(match.group(2))
            data_flags["mq2"] = True
        if match.group(3):  # MQ-3: Alcohol
            sensor_buffer["alcohol"] = float(match.group(3))
            data_flags["mq3"] = True
        if match.group(4) and match.group(5):  # MQ-5: LPG and Methane
            sensor_buffer["lpg"] = float(match.group(4))  # Overwrite LPG from MQ-2 if present
            sensor_buffer["methane"] = float(match.group(5))
            data_flags["mq5"] = True
        if match.group(6) and match.group(7):  # MQ-9: CO and Flammable Gases
            sensor_buffer["co"] = float(match.group(6))
            sensor_buffer["flammable_gas"] = float(match.group(7))
            data_flags["mq9"] = True
        
        # Check if all sensors have reported or if timeout has passed
        if all(data_flags.values()) or time.time() - start_time >= timeout_duration:
            # Add timestamp to the data
            sensor_buffer["timestamp"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Write data to JSON (gas.json with timestamp)
            write_to_json(sensor_buffer.copy())
            # Reset buffer and flags for the next cycle
            reset_buffer_and_flags()

def reset_buffer_and_flags():
    """Reset the sensor buffer and data flags for the next cycle."""
    global sensor_buffer, data_flags, start_time
    sensor_buffer = {
        "lpg": None,
        "smoke": None,
        "alcohol": None,
        "methane": None,
        "co": None,
        "flammable_gas": None,
        "timestamp": None
    }
    data_flags = {
        "mq2": False,
        "mq3": False,
        "mq5": False,
        "mq9": False
    }
    start_time = time.time()  # Reset the timer for the next cycle

try:
    while ser and ser.is_open:
        if ser.in_waiting > 0:
            print("Reading serial data...")

            raw_data = ser.readline().decode('utf-8').strip()
            print(f"Raw data received: {raw_data}")

            # Process the raw data
            process_data(raw_data)

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    print("Process interrupted by user.")

finally:
    if ser and ser.is_open:
        ser.close()
        print("Serial connection closed.")
