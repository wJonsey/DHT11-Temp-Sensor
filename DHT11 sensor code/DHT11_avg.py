import time
import board
import adafruit_dht
import csv
from datetime import datetime
import os



# CSV
filename = "DHT11_log.csv"


def safe_write_row(main_file, row):
    temp_file = "temp_log.csv"

    with open(temp_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    with open(main_file, "a", newline="") as main, open(temp_file, "r") as temp:
        main.write(temp.read())

    os.remove(temp_file)


# Create CSV 
try:
    with open(filename, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "avg_temp", "avg_humidity"])
except FileExistsError:
    pass

# GPIO 27
dht_device = adafruit_dht.DHT11(board.D27)

try:
    while True:
        temp_readings = []
        hum_readings = []

        start_time = time.time()

        # seconds only
        current_seconds = int(time.time()) 

        # every 40 seconds
        if current_seconds % 40 == 0:
            try:
                temp = dht_device.temperature
                hum = dht_device.humidity

                if temp is not None and hum is not None:
                    temp_readings.append(temp)
                    hum_readings.append(hum)

            except RuntimeError:
                pass

            #averages
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

            # waits
            time.sleep(1)

except KeyboardInterrupt:
    print("Stopping program...")

finally:
    dht_device.exit()
