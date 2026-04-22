import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/workspaces/projects/csv/DHT11_log.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values("Timestamp")


df["temp_smooth"] = df["avg_temp"].rolling(5, center=True).mean()
df["hum_smooth"] = df["avg_humidity"].rolling(5, center=True).mean()


def risk_score(t, h):
    if t < 14:
        return 20
    elif h < 82:
        return 60
    else:
        return 90

df["risk"] = df.apply(lambda r: risk_score(r["avg_temp"], r["avg_humidity"]), axis=1)
df["risk_smooth"] = df["risk"].rolling(5, center=True).mean()


fig, ax1 = plt.subplots(figsize=(12,6))


ax1.plot(df["Timestamp"], df["temp_smooth"],
         color="darkred", alpha=0.7, label="Temperature (°C)")
ax1.set_ylabel("Temperature (°C)", color="darkred")


ax2 = ax1.twinx()
ax2.plot(df["Timestamp"], df["hum_smooth"],
         color="royalblue", alpha=0.7, label="Humidity (%)")
ax2.set_ylabel("Humidity (%)", color="royalblue")


ax3 = ax1.twinx()
ax3.spines["right"].set_position(("outward", 60))
ax3.plot(df["Timestamp"], df["risk_smooth"],
         color="green", linewidth=2.5, label="Mildew Risk")
ax3.set_ylabel("Risk (0–100)", color="green")
ax3.set_ylim(0, 100)


ax3.axhspan(0, 40, color="green", alpha=0.1)
ax3.axhspan(40, 70, color="orange", alpha=0.1)
ax3.axhspan(70, 100, color="red", alpha=0.1)


plt.title("🌿 Strawberry Powdery Mildew Risk (DHT11 Sensor Data)")
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig('DHT_graph.png')
plt.show()