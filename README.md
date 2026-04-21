# 🍓 DHT11 Strawberry Mildew Monitor

A lightweight Flask dashboard that reads live temperature and humidity from a DHT11 sensor and calculates the risk of **Powdery Mildew** on strawberry crops. Runs on any Raspberry Pi with a DHT11 sensor attached.

---

## Features

- 📊 **Live web dashboard** — auto-refreshes every 3 seconds, no CSV or database needed
- 🌿 **Mildew risk score** — calculates a 0–100 risk index based on real sensor readings
- 📱 **Telegram alerts** — sends instant free notifications to your phone when risk is elevated
- 🎨 **Visual dashboard** — dark botanical UI with colour-coded risk meter and status banner
- ⚡ **Lightweight** — runs entirely on the Pi, no cloud services required

---

## How It Works

The sensor reads temperature and humidity every 3 seconds. A simple risk model scores conditions:

| Condition | Risk Score |
|---|---|
| Temperature below 14°C | 20 — Low |
| Humidity below 82% | 60 — Moderate |
| Humidity 82%+ (warm) | 90 — Critical |

When the risk crosses a threshold, a Telegram message is sent to your phone. Alerts are smart — they won't spam you, only firing once per risk level change.

---

## Hardware Required

- Raspberry Pi (any model)
- DHT11 temperature & humidity sensor
- Sensor wired to **GPIO 17 and GPIO 27**

---

## Installation

**1. Clone the repo**
```bash
git clone https://github.com/20188948/DHT11-Temp-Sensor.git
cd DHT11-Temp-Sensor
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up Telegram alerts** *(optional but recommended)*

See [`telegram_setup_instructions.txt`](telegram_setup_instructions.txt) for a full step-by-step guide.

Once you have your bot token and chat ID, open `mildew_monitor.py` and fill in:
```python
TELEGRAM_TOKEN   = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
```

**4. Run**
```bash
python mildew_monitor.py
```

Then open a browser on any device on the same network and go to:
```
http://<your-pi-ip>:5000
```

---

## Dependencies

```
Adafruit_DHT
adafruit-circuitpython-dht
flask
requests
pandas
matplotlib
board
```

---

## Dashboard Preview

The dashboard shows live temperature, humidity, and a colour-coded risk meter that shifts from green → orange → red as conditions worsen.

- **Green** — Low risk (score below 50)
- **Orange** — Moderate risk (score 50–79)
- **Red** — Critical risk (score 80+)

---

## Project Structure

```
DHT11-Temp-Sensor/
├── mildew_monitor.py              # Main Flask app + sensor logic + Telegram alerts
├── requirements.txt               # Python dependencies
└── telegram_setup_instructions.txt  # Step-by-step Telegram bot guide
```

---

## License

MIT — free to use, modify, and distribute.
