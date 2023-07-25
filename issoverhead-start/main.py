import requests
from datetime import datetime
import smtplib
import time

MY_LAT = -37.813629 # Your latitude
MY_LONG = 144.963058 # Your longitude

my_email = "sun.melinda888@gmail.com"
password = "hvzdmopimfuxdtdq"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    iss_data = response.json()
    print(iss_data)

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude<= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    else:
        return False

def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    mel_data = response.json()
    print(mel_data)
    sunrise = int(mel_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(mel_data["results"]["sunset"].split("T")[1].split(":")[0])
    print(sunrise)
    print(sunset)

    time_now = datetime.now().hour
    print(time_now)
    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False

#If the ISS is close to my current position


# and it is currently dark

# Then send me an email to tell me to look up.
def my_function():

    is_in_mel = is_iss_overhead()
    dark_now = is_dark()
    if is_in_mel == True and dark_now == True:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="sun.melinda@myyahoo.com",
                msg="Subject:Look Up👆\n\nThe ISS is above you in the sky.")
# BONUS: run the code every 60 seconds.
my_function()
time.sleep(60)



