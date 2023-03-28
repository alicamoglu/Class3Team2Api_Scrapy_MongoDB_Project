from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
import sys
import requests, pymongo
from pymongo import *
from Ui_weather_proje import *
from PyQt5.QtCore import QDateTime, Qt


class Main_Class(QMainWindow,  Ui_MainWindow):
    def __init__(self):
        super(Main_Class, self).__init__()
        self.setupUi(self)
        self.label_gif.setFixedSize(100,100)
        
        
        self.client = pymongo.MongoClient("mongodb+srv://sumeyra:1234@cluster0.rvan9sx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["weather_app"]
        self.collection = self.db["weather_infos"]
        self.city_germany = self.db["germany"]
        self.city_america = self.db["america"]
        self.city_netherland = self.db["netherland"]
        self.movie = QtGui.QMovie("world.gif")
        self.movie.setScaledSize(QtCore.QSize(100, 100))
    
        self.table_cities.cellClicked.connect(self.get_weather)
        self.comboBox_country.currentTextChanged.connect(self.get_cities)
        self.table_cities.itemSelectionChanged.connect(self.get_city_info_germany)
        self.table_cities.itemSelectionChanged.connect(self.get_city_info_netherland)
        self.table_cities.itemSelectionChanged.connect(self.get_city_info_usa)
        self.Button_find.clicked.connect(self.search_city)
        self.label_gif.setMovie(self.movie)
        self.movie.start()
        
    def get_weather(self, row, column):
        current_row = self.table_cities.currentRow()
        current_column = self.table_cities.currentColumn()
        city_name = self.table_cities.item(current_row, current_column).text()

        self.label_city_name_show.setText(city_name) 
              
        api_key = '1c50e484391dc9fbbaa60f8c4ef4c22b'
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric")
        
#parse json data
        
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        humidity = weather_data.json()['main']['humidity']
        wind_speed = round(weather_data.json()['wind']['speed'],1)
        pressure = weather_data.json()['main']['pressure']
        icon = weather_data.json()['weather'][0]['icon']
        datetime = QDateTime.currentDateTime()
        print(weather_data.json())                            # here content of the weather_data is seen in console to nevigate for target data
        #print("-------------------------")                   # seperator
        #print(icon)                                          # here for check in console if it brings accurate weather situation icon

#fill the ui label
        self.label_temperature.setText(str(temp)+"°C")
        self.label_huminity.setText(str(humidity)+"%")
        self.label_wind.setText(str(wind_speed)+" km/h")
        self.label_pressure.setText(str(pressure)+" mb")
        self.label_icon_situation.setPixmap(QtGui.QPixmap(f":/newPrefix/{icon}.png"))     #label_icon_situation is send here
        self.label_update.setText(datetime.toString(Qt.DefaultLocaleLongDate)) # label_update is send here

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
    
    def get_cities(self):
        
        selected_country = self.comboBox_country.currentText()
        #print(selected_country)
        if selected_country == "USA" :
            self.get_america()
        elif selected_country == "Germany":
            self.get_germany()
        elif selected_country == "Netherlands":
            self.get_netherland()
            
            
            
    def get_germany(self):
        data_cities = self.city_germany.find({"country" : "Germany"},{'city' :1,'region':1, 'population':1})
        rows_data=[]
        for result in data_cities:
            rows_data.append(result)
            
       
        row = 0
        self.table_cities.setRowCount(len(rows_data))
        for result in rows_data:
            self.table_cities.setItem(row, 0, QtWidgets.QTableWidgetItem(result["city"]))
            self.table_cities.setItem(row, 1, QtWidgets.QTableWidgetItem(result["region"]))
            self.table_cities.setItem(row, 2, QtWidgets.QTableWidgetItem(str(result["population"])))
            row +=1   
            
       
    def get_america(self):
               
        data_cities = self.city_america.find({"country" : "USA"},{'city' :1,'region':1,'population':1})
        rows_data=[]
        for result in data_cities:
            rows_data.append(result)
            
        row = 0
        self.table_cities.setRowCount(len(rows_data))
        for result in rows_data:
            self.table_cities.setItem(row, 0, QTableWidgetItem(result["city"]))
            self.table_cities.setItem(row, 1, QTableWidgetItem(result["region"]))
            self.table_cities.setItem(row, 2, QTableWidgetItem(str(result["population"])))
            row +=1  
        #for i in self.city_america.find():
            #print(i)
        
    def get_netherland(self):
        data_cities = self.city_netherland.find({"country" : "Netherland"},{'city' :1,'region':1,'population':1})
        rows_data=[]
        for result in data_cities:
            rows_data.append(result)
            
        row = 0
        self.table_cities.setRowCount(len(rows_data))
        for result in rows_data:
            self.table_cities.setItem(row, 0, QTableWidgetItem(result["city"]))
            self.table_cities.setItem(row, 1, QTableWidgetItem(result["region"]))
            self.table_cities.setItem(row, 2, QTableWidgetItem(str(result["population"])))
            row +=1  
        
    def get_city_info_germany(self):
        selected_items = self.table_cities.selectedItems()
        if len(selected_items) == 0:  #If there is no selected item, the function terminates with return.
            return    

        selected_city = selected_items[0].text()
        query = {"country": "Germany", "city": selected_city} #The text value of the selected item is assigned to the selected_city variable.
        city_info = self.city_germany.find_one(query)
        if not city_info:
            return

        self.label_country_info.setText("Germany")
        self.label_region_info.setText(city_info["region"])
        self.label_population_info.setText(str(city_info["population"])) 

    def get_city_info_netherland(self):    
        selected_items = self.table_cities.selectedItems()
        if len(selected_items) == 0:  
            return
        
        selected_city = selected_items[0].text()
        query = {"country": "Netherland", "city": selected_city}
        city_info = self.city_netherland.find_one(query)
        if not city_info:
            return

        self.label_country_info.setText("Netherland")
        self.label_region_info.setText(city_info["region"])
        self.label_population_info.setText(str(city_info["population"])) 

    def get_city_info_usa(self):    
        selected_items = self.table_cities.selectedItems()
        if len(selected_items) == 0:   
            return
        
        selected_city = selected_items[0].text()
        query = {"country": "USA", "city": selected_city}
        city_info = self.city_america.find_one(query)
        if not city_info:
            return

        self.label_country_info.setText("USA")
        self.label_region_info.setText(city_info["region"])
        self.label_population_info.setText(str(city_info["population"]))    
    
    def search_city(self):
        self.city = self.lineEdit_city.text()
        if len(self.city) == 0 :
            return
        
        myquery = {"city": self.city}
        search_city_german= self.city_germany.find(myquery)
        search_city_netherland = self.city_netherland.find(myquery)
        search_city_america = self.city_america.find(myquery)
        for x in search_city_german:
            self.label_country_info.setText("Germany")
            self.label_region_info.setText(x["region"])
            self.label_population_info.setText(str(x["population"])) 
            
        for x in search_city_netherland:
            self.label_country_info.setText("Netherland")
            self.label_region_info.setText(x["region"])
            self.label_population_info.setText(str(x["population"]))
                   
        for x in search_city_america:
            self.label_country_info.setText("USA")
            self.label_region_info.setText(x["region"])
            self.label_population_info.setText(str(x["population"]))
            
       
        self.label_city_name_show.setText(self.city) 
        api_key = '1c50e484391dc9fbbaa60f8c4ef4c22b'
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={api_key}&units=metric")
        
#parse json data
        # print(weather_data.json())
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        humidity = weather_data.json()['main']['humidity']
        wind_speed = round(weather_data.json()['wind']['speed'],1)
        pressure = weather_data.json()['main']['pressure']
        icon = weather_data.json()['weather'][0]['icon']
        print(weather_data.json())                            # here content of the weather_data is seen in console to nevigate for target data
        print("-------------------------")                   # seperator
        print(icon)                                          # here for check in console if it brings accurate weather situation icon
#fill the ui label
        self.label_temperature.setText(str(temp)+"°C")
        self.label_huminity.setText(str(humidity)+"%")
        self.label_wind.setText(str(wind_speed)+" km/h")
        self.label_pressure.setText(str(pressure)+" mb")
        self.label_icon_situation.setPixmap(QtGui.QPixmap(f":/newPrefix/{icon}.png"))     #label_icon_situation is send here

# #insert to mongodb database
        item = {
            "country" : self.label_country_info.text(),
            "city_name" : self.city,
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
    widget.setFixedHeight(890)
    widget.setFixedWidth(990)
    widget.show()

    try:
        sys.exit(app.exec_())

    except:
        print("Exiting")
    
