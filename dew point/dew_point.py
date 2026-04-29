import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

df = pd.read_csv('/workspaces/projects/csv/DHT11_log.csv')

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df = df.sort_values('Timestamp')

def dew_point(temp_c, humidity):
    a = 17.27
    b = 237.7
    gamma = (a * temp_c) / (b + temp_c) + math.log(humidity / 100.0)
    return (b * gamma) / (a - gamma)

df['dew_point'] = df.apply(
    lambda r: dew_point(r['avg_temp'], r['avg_humidity']),
    axis=1
)

def mildew_risk(temp, humidity, dew_point):
    risk = 0
    if 60 <= humidity <= 90:
        risk += 1
    if humidity > 90:
        risk += 2
    if 15 <= temp <= 25:
        risk += 1
    if abs(temp - dew_point) < 2:
        risk += 1
    return min(risk, 3)

df['mildew_risk'] = df.apply(
    lambda r: mildew_risk(r['avg_temp'], r['avg_humidity'], r['dew_point']),
    axis=1
)



fig, ax = plt.subplots()

ax.plot(df['Timestamp'], df['avg_temp'], label='Temperature')
ax.plot(df['Timestamp'], df['dew_point'], label='Dew Point')

ax.set_xlabel('Time')
ax.set_ylabel('°C')
ax.set_title('Temperature, Dew Point & Mildew Risk')


for i in range(len(df) - 1):
    if df['mildew_risk'].iloc[i] == 0:
        color = 'green'
    elif df['mildew_risk'].iloc[i] == 1:
        color = 'yellow'
    elif df['mildew_risk'].iloc[i] == 2:
        color = 'orange'
    else:
        color = 'red'

    ax.axvspan(df['Timestamp'].iloc[i],
               df['Timestamp'].iloc[i + 1],
               color=color,
               alpha=0.08)


ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45)

ax.legend()
plt.tight_layout()

plt.savefig('dew_point_mildew_risk.png', dpi=300)
plt.show()