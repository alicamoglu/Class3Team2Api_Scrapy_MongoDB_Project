from PyQt5.QtWidgets import *
import sys
import requests
import pymongo


from Ui_weather_proje import *

class Main_Class(QMainWindow,  Ui_MainWindow):
    def __init__(self):
        super(Main_Class, self).__init__()
        self.setupUi(self)
        self.table_cities.cellClicked.connect(self.get_weather)

        
        self.client = pymongo.MongoClient("mongodb+srv://sumeyra:1234@cluster0.rvan9sx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["weather_app"]
        self.collection = self.db["weather_infos"]
    
    def get_weather(self, row, column):
        current_row = self.table_cities.currentRow()
        current_column = self.table_cities.currentColumn()
        city_name = self.table_cities.item(current_row, current_column).text()
               
        api_key = '1c50e484391dc9fbbaa60f8c4ef4c22b'
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric")

#parse json data
        # print(weather_data.json())
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        humidity = weather_data.json()['main']['humidity']
        wind_speed = round(weather_data.json()['wind']['speed'],1)
        pressure = weather_data.json()['main']['pressure']

#fill the ui label
        self.label_temperature.setText(str(temp)+"^C")
        self.label_huminity.setText(str(humidity))
        self.label_wind.setText(str(wind_speed))
        self.label_pressure.setText(str(pressure))

# #insert to mongodb database
        item = {
            "country" : self.label_country_info.text(),
            "city_name" : city_name,
            "temperature" : temp,
            "humidity" : humidity,
            "wind_speed" : wind_speed,
            "pressure" : pressure
        }

        try:
            self.collection.insert_one(item)
        except pymongo.errors.WriteError as e:
            print("Save Error : ", e)


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
    
