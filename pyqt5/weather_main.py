from PyQt5.QtWidgets import *
import sys
import requests


from Ui_weather_proje import *

class Main_Class(QMainWindow,  Ui_MainWindow):
    def __init__(self):
        super(Main_Class, self).__init__()
        self.setupUi(self)
        self.comboBox_city.currentTextChanged.connect(self.get_weather)
    
    
    def get_weather(self,city_name):
        

        api_key = '1c50e484391dc9fbbaa60f8c4ef4c22b'

        #city_name = input("City Name")
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric")

        #    f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&APPID={api_key}")

        print(weather_data.json())
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        humidity = weather_data.json()['main']['humidity']
        # resilince =
        wind_speed = round(weather_data.json()['wind']['speed'],1)

        print(weather, temp, humidity,wind_speed)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = Main_Class()
    widget = QtWidgets.QStackedWidget()
    
    widget.addWidget(mainwindow)

    widget.show()

    try:
        sys.exit(app.exec_())

    except:
        print("Exiting")
    
