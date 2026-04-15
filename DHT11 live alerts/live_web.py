from flask import Flask
import board
import adafruit_dht
import time

app = Flask(__name__)

# DHT11 on GPIO17
dht = adafruit_dht.DHT11(board.D17)

def risk_score(temp, hum):
    if temp is None or hum is None:
        return 0
    if temp < 14:
        return 20
    elif hum < 82:
        return 60
    else:
        return 90


def read_sensor():
    try:
        temp = dht.temperature
        hum = dht.humidity
        return temp, hum
    except RuntimeError:
        return None, None


@app.route("/")
def home():

    temp, hum = read_sensor()

    # retry once if failed
    if temp is None or hum is None:
        time.sleep(1)
        temp, hum = read_sensor()

    if temp is None or hum is None:
        return "<h1>Sensor reading failed</h1>"

    risk = risk_score(temp, hum)

    color = "green"
    if risk >= 80:
        color = "red"
    elif risk >= 50:
        color = "orange"

    return f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="3">
        <title>Mildew Monitor Live</title>
    </head>

    <body style="font-family: Arial; text-align: center;">
        <h1>🌿 Strawberry Mildew Monitor (LIVE)</h1>

        <h2>🌡 Temperature: {temp} °C</h2>
        <h2>💧 Humidity: {hum} %</h2>

        <h2 style="color:{color}; font-size:32px;">
            🌿 Risk: {risk}/100
        </h2>

        <p>Live GPIO reading (no CSV used)</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)