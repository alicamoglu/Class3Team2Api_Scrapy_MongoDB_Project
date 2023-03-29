import datetime
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
import sys
import requests, pymongo
from pymongo import *
from Ui_weather_proje import *
from PyQt5.QtCore import QDateTime, Qt

# rows_data = []

class Main_Class(QMainWindow,  Ui_MainWindow):
    def __init__(self):
        super(Main_Class, self).__init__()
        self.setupUi(self)
        self.label_gif.setFixedSize(100, 100)
        
        self.client = pymongo.MongoClient("mongodb+srv://sumeyra:1234@cluster0.rvan9sx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["weather_app"]
        self.collection = self.db["weather_infos"]
        self.city_germany = self.db["germany"]
        self.city_america = self.db["america"]
        self.city_netherland = self.db["netherland"]
        self.movie = QtGui.QMovie("world.gif")
        self.movie.setScaledSize(QtCore.QSize(100, 100))
        self.label_gif.setMovie(self.movie)
        self.table_cities.setColumnWidth(0,170)
        self.table_cities.setColumnWidth(1,170)
        self.table_cities.setColumnWidth(2,150)
        
        self.table_cities.cellClicked.connect(self.get_weather)
        self.comboBox_country.currentTextChanged.connect(self.get_cities)
        self.table_cities.itemSelectionChanged.connect(self.get_city_info_germany)
        self.table_cities.itemSelectionChanged.connect(self.get_city_info_netherland)
        self.table_cities.itemSelectionChanged.connect(self.get_city_info_usa)
        self.Button_find.clicked.connect(self.search_city)
        self.Button_filter.clicked.connect(self.filter)
        self.label_gif.setMovie(self.movie)
        self.movie.start()
        
    def get_weather(self, row, column):
        current_row = self.table_cities.currentRow()
        current_column = self.table_cities.currentColumn()
        city_name = self.table_cities.item(current_row, current_column).text()

        self.label_city_name.setText(city_name) 
              
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
        icon = weather_data.json()['weather'][0]['icon']
        datetime = QDateTime.currentDateTime()
        print(weather_data.json())                            # here content of the weather_data is seen in console to nevigate for target data
        #print("-------------------------")                   # seperator
        #print(icon)                                          # here for check in console if it brings accurate weather situation icon
#fill the ui label
        self.label_weather.setText(str(weather).upper())
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
        self.lineEdit_city.clear()
        data_cities = self.city_germany.find({"country" : "Germany"},{'city' :1,'region':1, 'population':1})
        global rows_data
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
        self.label_source.setText("https://de.wikipedia.org/wiki/Liste_der_Gro%C3%9F-_und_Mittelst%C3%A4dte_in_Deutschland")    
       
    def get_america(self):
        self.lineEdit_city.clear()
        global rows_data       
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
        self.label_source.setText("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population")    
        
    def get_netherland(self):
        self.lineEdit_city.clear()
        global rows_data
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
        self.label_source.setText("https://tr.wikipedia.org/wiki/Hollanda%27daki_%C5%9Fehirler_listesi")
        
        
    def filter(self):
        self.table_cities.clear()
        # data_cities = self.city_germany.find({"country" : "Germany"},{'city' :1,'region':1, 'population':1})
        # rows_data=[]
        # for result in data_cities:
        #     rows_data.append(result)
        # rows_data = self.get_germany.rows_data   
        filterEnteryCity = self.lineEdit.text()  #self.city = self.lineEdit_city.text()
        filterEnteryRegion = self.lineEdit_2.text()  #self.city = self.lineEdit_city.text()

        CapitalCityFilter = ""
        CapitalRegionFilter = ""
        if len(filterEnteryCity) != 0:
            CapitalCityFilter = filterEnteryCity[0].upper() + filterEnteryCity[1:len(filterEnteryCity)].lower()
        if len(filterEnteryRegion) != 0:
            CapitalRegionFilter = filterEnteryRegion[0].upper() + filterEnteryRegion[1:len(filterEnteryRegion)].lower()
        row = 0
        self.table_cities.setRowCount(len(rows_data))
        for result in rows_data:

            if (filterEnteryCity.lower() not in result["city"] and CapitalCityFilter not in result["city"]):
                continue
                # result["city"].setShowGrid(False) #  AttributeError: 'str' object has no attribute 'setShowGrid'
            if (filterEnteryRegion.lower() not in result["region"] and CapitalRegionFilter not in result["region"]):
                continue  
            self.table_cities.setItem(row, 0, QtWidgets.QTableWidgetItem(result["city"]))
            self.table_cities.setItem(row, 1, QtWidgets.QTableWidgetItem(result["region"]))
            self.table_cities.setItem(row, 2, QtWidgets.QTableWidgetItem(str(result["population"])))
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
        self.label_country_info.clear()
        self.label_region_info.clear()
        self.label_population_info.clear()
        self.label_source.clear()
        self.label_city_name.clear()
        self.label_temperature.clear()
        self.label_huminity.clear()
        self.label_wind.clear()
        self.label_pressure.clear()
        self.label_update.clear()
        self.label_weather.clear()
        self.label_icon_situation.clear()
        self.city = self.lineEdit_city.text()
        if len(self.city) == 0 :
            return
        
        
        search_city_germany= self.city_germany.find({"city": self.city},{"city" : 1, "region" :1, "population" :1})
        search_city_netherland= self.city_netherland.find({"city": self.city},{"city" : 1,  "region" :1, "population" :1})
        search_city_america= self.city_america.find({"city": self.city},{"city" : 1,  "region" :1, "population" :1})
        for x in search_city_germany:
            self.label_country_info.setText("Germany")
            self.label_region_info.setText(x["region"])
            self.label_population_info.setText(str(x["population"]))
            self.label_source.setText("https://de.wikipedia.org/wiki/Liste_der_Gro%C3%9F-_und_Mittelst%C3%A4dte_in_Deutschland")
            self.label_city_name.setText(self.city) 
            self.search_city_weather()
        for x in search_city_netherland:
            self.label_country_info.setText("Netherland")
            self.label_region_info.setText(x["region"])
            self.label_population_info.setText(str(x["population"]))
            self.label_city_name.setText(self.city)   
            self.label_source.setText("https://tr.wikipedia.org/wiki/Hollanda%27daki_%C5%9Fehirler_listesi") 
            self.search_city_weather()
        for x in search_city_america:
            self.label_country_info.setText("USA")
            self.label_region_info.setText(x["region"])
            self.label_population_info.setText(str(x["population"]))
            self.label_city_name.setText(self.city)
            self.label_source.setText("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population")
            self.search_city_weather()
            
        
            
            
    def search_city_weather(self):
        api_key = '1c50e484391dc9fbbaa60f8c4ef4c22b'
        weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={api_key}&units=metric")
        
        #parse json data
            # print(weather_data.json())
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        humidity = weather_data.json()['main']['humidity']
        wind_speed = round(weather_data.json()['wind']['speed'],1)
        pressure = weather_data.json()['main']['pressure']
        icon = weather_data.json()['weather'][0]['icon']
        datetime = QDateTime.currentDateTime()
        #print(weather_data.json())                            # here content of the weather_data is seen in console to nevigate for target data
        #print("-------------------------")                   # seperator
        #print(icon)                                          # here for check in console if it brings accurate weather situation icon
        #fill the ui label
        self.label_weather.setText(str(weather).upper())
        self.label_temperature.setText(str(temp)+"°C")
        self.label_huminity.setText(str(humidity)+"%")
        self.label_wind.setText(str(wind_speed)+" km/h")
        self.label_pressure.setText(str(pressure)+" mb")
        self.label_icon_situation.setPixmap(QtGui.QPixmap(f":/newPrefix/{icon}.png"))     #label_icon_situation is send here
        self.label_update.setText(datetime.toString(Qt.DefaultLocaleLongDate)) # label_update is send here
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
    
