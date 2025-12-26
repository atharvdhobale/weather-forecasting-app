from tkinter import *
from tkinter import messagebox as mb
from tkinter.scrolledtext import ScrolledText
import requests
from datetime import datetime

# Create the main window
root = Tk()
root.title('Automated Weather Forecasting App')
root.configure(bg='#2e2e2e')
root.geometry("850x800")

# Title label
title = Label(root, text='Automated Weather Detection and Forecast', fg='#f7f7f7', bg='#2e2e2e', font=("Helvetica", 18, "bold"))
title.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

# City input
label1 = Label(root, text='Enter City:', font=('Helvetica', 12), bg='#2e2e2e', fg='#f7f7f7')
label1.grid(row=1, column=0, padx=10, pady=10, sticky='E')
city_input = Entry(root, width=30, fg='black', font=12, relief=GROOVE)
city_input.grid(row=1, column=1, padx=5, pady=5)

# Labels for basic weather information
labels_texts = ["Temperature (°C):", "Pressure (hPa):", "Humidity (%):", "Wind Speed (m/s):", "Cloudiness (%):", "Description:"]
entries = []

for i, text in enumerate(labels_texts):
    label = Label(root, text=text, font=('Helvetica', 12), bg='#2e2e2e', fg='#f7f7f7')
    label.grid(row=i + 3, column=0, padx=10, pady=5, sticky='E')
    entry = Entry(root, width=30, font=('Helvetica', 12))
    entry.grid(row=i + 3, column=1, padx=5, pady=5)
    entries.append(entry)

# Function to get current weather
def get_weather():
    city = city_input.get()
    api_key = "YOUR_API_KEY_HERE" # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            cloud = data['clouds']['all']
            description = data['weather'][0]['description']

            for i, value in enumerate([temp, pressure, humidity, wind, cloud, description]):
                entries[i].delete(0, END)
                entries[i].insert(0, str(value))
        else:
            mb.showerror("Error", "City not found!")
    except Exception as e:
        mb.showerror("Error", f"Unable to get weather data.\nError: {e}")

# Forecast display area
forecast_area = ScrolledText(root, width=110, height=15, font=('Courier', 10), bg='#1e1e1e', fg='#00ff00')
forecast_area.grid(row=10, column=0, columnspan=3, padx=10, pady=10)

# Function to get weather forecast
def get_forecast():
    city = city_input.get()
    api_key = 'b5c04f2289c3a96adf292c6cd30dccf9'  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            forecast_area.delete(1.0, END)
            current_day = ""

            for item in data['list']:
                dt = datetime.utcfromtimestamp(item['dt'])
                day = dt.strftime('%A %d %B')

                if day != current_day:
                    forecast_area.insert(END, f"\n{day}\n{'-' * 80}\n")
                    current_day = day

                time = dt.strftime('%H:%M')
                temp = item['main']['temp']
                description = item['weather'][0]['description']
                wind_speed = item['wind']['speed']
                rain = item.get('rain', {}).get('3h', 0)
                humidity = item['main']['humidity']

                forecast_area.insert(END, f"{time} | {description.capitalize():<20} | Temp: {temp}°C | Wind: {wind_speed} km/h | Humidity: {humidity}% | Rain: {rain} mm\n")
        else:
            mb.showerror("Error", "City not found!")
    except Exception as e:
        mb.showerror("Error", f"Unable to get forecast data.\nError: {e}")

# Reset fields
def reset_fields():
    city_input.delete(0, END)
    for entry in entries:
        entry.delete(0, END)
    forecast_area.delete(1.0, END)

# Buttons
btn_submit = Button(root, text='Get Weather', width=15, font=('Helvetica', 12), bg='#4CAF50', fg='white', command=get_weather)
btn_forecast = Button(root, text='Get Forecast', width=15, font=('Helvetica', 12), bg='#4CAF50', fg='white', command=get_forecast)
btn_reset = Button(root, text='Reset', width=15, font=('Helvetica', 12), bg='#f44336', fg='white', command=reset_fields)

btn_submit.grid(row=2, column=0, pady=10)
btn_forecast.grid(row=2, column=1, pady=10)
btn_reset.grid(row=11, column=1, pady=10)

# Run the Tkinter loop
root.mainloop()
