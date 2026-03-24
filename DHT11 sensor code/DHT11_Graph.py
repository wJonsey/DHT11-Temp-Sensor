import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('DHT11_log.csv')

#30 minute conversion for timestamp every 30 minutes
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))



#setting axis
x = df["Timestamp"] 
y1 = df['avg_temp']
y2 = df['avg_humidity']


#plotting data
plt.plot (x,y1, label = 'Temperature'   )
plt.plot (x,y2, label = 'Humidity'    )
plt.ylabel('Temperature')
plt.xlabel('Timestamp')




#saving and doing layout
plt.suptitle('DHT11 Sensor Data')
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.savefig('Dht11_graph.png')
plt.show()
