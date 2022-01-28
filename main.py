import requests
from datetime import datetime
import smtplib


MY_LAT = 5.527940  # Your latitude
MY_LONG = 7.494460  # Your longitude
MY_EMAIL = 'obipedrochinomso@gmail.com'
MY_PASSWORD = 'pedroski121'


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.


def within_position():
    if MY_LAT - iss_latitude <= 5 and MY_LAT - iss_latitude >= -5:
        if MY_LONG - iss_longitude <= 5 and MY_LONG - iss_longitude >= -5:
            return True
    return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get(
    "https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
current_hour = time_now.hour


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


def dark():
    if current_hour >= sunset or current_hour <= sunrise:
        return True
    else:
        return False


if within_position() and dark():
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL, to_addrs='obipedro121@gmail.com', msg="Subject:ISS \n\n Lookup")
    print('Email Sent')
