# import the necessary modules
import io
import os
import json
import requests
from PIL import Image, ImageTk
from tkinter import Tk, Label, Entry, Button

# Font Format
FONT = ("Arial bold ",12)

# Main window
root = Tk()
root.title("Musbi's Weather App")
root.geometry('400x300+300+120')
root.resizable(False, False)

# city label
user_city = Label(text="Enter City Name:", font=FONT)
user_city.grid(row=0, column=0)

#user entry
user_input = Entry(root)
user_input.grid(row=0, column=1)

# fetch weather button
fetch_btn = Button(text="Fetch Now!", font=FONT)
fetch_btn.grid(row=1, column=0, columnspan=3)

# result
result = Label(text="", font=FONT)
result.grid(row=2, column=0, columnspan=4)

icon_label = Label(root)
icon_label.grid(row=3, column=0, columnspan=4)

def weather_checker():
    city = user_input.get()
    api_key = os.getenv('api_key')
    print(api_key)
    url = "https://api.openweathermap.org/data/2.5/weather?"
    params = {
        "q":city,
        "appid":api_key,
        "units":"metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)

    # fetch the weather data if the user enter a valid city address
    if response.status_code == 200:
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        speed = data['wind']['speed']
        country_code = data['sys']['country']
        city_name = data['name']
        icon_code = data['weather'][0]['icon']
        print(weather)
        print(temp)
        print(humidity)
        print(speed)
        print(country_code)
        print(city_name)

        # display the result
        result.config(text=f"Weather: {weather}\nTemp: {temp}°C\nHumidity: {humidity}\n"
                           f"Speed: {speed}\nCountry Code: {country_code}\nCity Name: {city_name}")

        # download the images
        # Download and show icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_data = requests.get(icon_url).content
        image = Image.open(io.BytesIO(icon_data))
        photo = ImageTk.PhotoImage(image)

        icon_label.config(image=photo)
        icon_label.image = photo  # Keep a reference to prevent garbage collection


        # send the user error message if they not enter a valid city address
    else:
        result.config(text="Error: Wrong city name or API issue!")
        icon_label.config(image="") # Clear icon if error

# fetch the current city weather
fetch_btn.config(command=weather_checker)


# show the main window
root.mainloop()