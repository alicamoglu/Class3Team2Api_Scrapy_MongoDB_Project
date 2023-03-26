import requests
import sys
import json
# -----------------------------API_key = '01102ac1e7aabc6cacb7f0fcde8cf9cc'


# lat = "48.414140"
# lon = "8.450130"
# part = "current"
# ------------request_url = 'https://api.openweathermap.org/data/2.5/weather?q=London&appid=01102ac1e7aabc6cacb7f0fcde8cf9cc'
# request_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API_key}"
# request_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_key}"
# request_url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=39.099724&lon=-94.578331&dt=1643803200&appid={API_key}"

# url = 'https://api.openweathermap.org'
# url = 'https://openweathermap.org/img/wn/10d@2x.png'
# url = "https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2"
api_key = '1c50e484391dc9fbbaa60f8c4ef4c22b'
city_name = 'kayseri'
weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric")
print(weather_data)
print(weather_data.json())

# ------------response = requests.get(request_url)#, params={

# -----------print(response)
# print(response)
# -----------------data = response.json()
# ------------------print(data)


# def jprint(obj):
#     # create a formatted string of the Python JSON object
#     text = json.dumps(obj, sort_keys=True, indent=4)
#     print(text)

# jprint(response.json())
