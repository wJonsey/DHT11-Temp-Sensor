                             
import time
import board
import adafruit_dht
import csv
from datetime import datetime

# File name
filename = "DHT11_log.csv"

# Create file with headers if it doesn't exist
try:
    with open(filename, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "avg_temp", "avg_humidity"])
except FileExistsError:
    pass
                                    
dht_device = adafruit_dht.DHT11(board.D17)

try:
    while True:
        temp_readings = []
        hum_readings = []

        start_time = time.time()

        # Collect readings for 40 seconds
        while (time.time() - start_time) < 40:
            try:
                temp = dht_device.temperature
                hum = dht_device.humidity

                if temp is not None and hum is not None:
                    # Optional: filter unrealistic values
                    if 0 <= temp <= 50 and 20 <= hum <= 90:
                        temp_readings.append(temp)
                        hum_readings.append(hum)

            except RuntimeError:
                # DHT11 errors are common — ignore and continue
                pass

            time.sleep(2)

        # Process results
        if temp_readings and hum_readings:
            avg_temp = round(sum(temp_readings) / len(temp_readings),2)
            avg_hum = round(sum(hum_readings) / len(hum_readings),2)

            print(f"40s Avg Temp: {avg_temp:.2f}°C  Avg Humidity: {avg_hum:.2f}%")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save to CSV
            with open(filename, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp,avg_temp,avg_hum])

        else:
            print("No valid readings collected in 40 seconds")

        print("-" * 40)

except KeyboardInterrupt:
    print("Stopping program...")

finally:
    dht_device.exit()
