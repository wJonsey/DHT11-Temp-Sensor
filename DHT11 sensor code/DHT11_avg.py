import time
import board
import adafruit_dht
import csv
from datetime import datetime
import os



# CSV file name
filename = "DHT11_log.csv"


def safe_write_row(main_file, row):
    temp_file = "temp_log.csv"

    # Step 1: write to temp file
    with open(temp_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    # Step 2: append temp file to main file
    with open(main_file, "a", newline="") as main, open(temp_file, "r") as temp:
        main.write(temp.read())

    # Step 3: remove temp file
    os.remove(temp_file)


# Create CSV with headers if it doesn't exist
try:
    with open(filename, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "avg_temp", "avg_humidity"])
except FileExistsError:
    pass

# Setup DHT11 on GPIO17 (pin 11)
dht_device = adafruit_dht.DHT11(board.D17)

try:
    while True:
        temp_readings = []
        hum_readings = []

        start_time = time.time()

        # Get integer seconds only
        current_seconds = int(time.time()) 

        # Trigger the block when seconds % 40 == 0
        if current_seconds % 40 == 0:
            try:
                temp = dht_device.temperature
                hum = dht_device.humidity

                if temp is not None and hum is not None:
                    temp_readings.append(temp)
                    hum_readings.append(hum)

            except RuntimeError:
                pass

            # Compute averages
            if temp_readings and hum_readings:
                avg_temp = round(sum(temp_readings) / len(temp_readings), 2)
                avg_hum = round(sum(hum_readings) / len(hum_readings), 2)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"40s Avg Temp: {avg_temp:.2f}°C  Avg Humidity: {avg_hum:.2f}%")
                # Save to CSV with full timestamp
                safe_write_row(filename, [timestamp, avg_temp, avg_hum])

            else:
                print("No valid readings collected in 40 seconds")

            print("-" * 40)

            # Wait before checking seconds again to avoid multiple triggers
            time.sleep(1)

except KeyboardInterrupt:
    print("Stopping program...")

finally:
    dht_device.exit()
