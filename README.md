# 🌡️ Raspberry Pi DHT11 Temperature & Humidity Monitor

A lightweight project that uses a Raspberry Pi and DHT11 sensor to read and display real-time temperature and humidity data.

---

## 📌 Overview

This project demonstrates how to interface a DHT11 sensor with a Raspberry Pi to collect environmental data. It’s ideal for beginners learning GPIO, sensor integration, and basic Python scripting.

---

## 🧰 Hardware Requirements

* Raspberry Pi (any model with GPIO support)
* DHT11 Temperature & Humidity Sensor
* 10kΩ resistor (if not included with sensor module)
* Jumper wires
* Breadboard (optional)

---

## 🔌 Wiring Diagram

| DHT11 Pin  | Connect To Raspberry Pi |
| ---------- | ----------------------- |
| VCC (+)    | 3.3V (Pin 1)            |
| DATA (OUT) | GPIO4 (Pin 7)           |
| GND (–)    | GND (Pin 6)             |

> ⚠️ Note: Use a 10kΩ pull-up resistor between VCC and DATA if your sensor does not include one.

---

## 💻 Software Setup

### 1. Update your system

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install dependencies

```bash
pip install Adafruit_DHT
```

---

## ▶️ Usage

Create a Python script (e.g., `main.py`) and add:

```python
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4  # GPIO4

humidity, temperature = Adafruit_DHT.read(sensor, pin)

if humidity is not None and temperature is not None:
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
else:
    print("Failed to retrieve data from sensor")
```

Run the script:

```bash
python main.py
```

---

## 📊 Example Output

```
Temperature: 23°C
Humidity: 55%
```

---

## ⚠️ Troubleshooting

* Ensure correct wiring (especially DATA pin)
* Check that the sensor is powered (3.3V recommended)
* Verify GPIO pin number in code matches your wiring
* Some readings may fail occasionally — this is normal for DHT11 sensors

---

## 🚀 Future Improvements

* Log data to a file or database
* Display readings on a web dashboard
* Add support for DHT22 (higher accuracy)
* Integrate with IoT platforms (e.g., MQTT, Home Assistant)

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🙌 Acknowledgements

* Adafruit DHT library
* Raspberry Pi Foundation documentation
