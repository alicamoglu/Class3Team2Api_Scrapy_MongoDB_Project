from PyQt5.QtWidgets import *
import sys
import requests, pymongo
from pymongo import *
from Ui_weather_proje import *

class Main_Class(QMainWindow,  Ui_MainWindow):
    def __init__(self):
        super(Main_Class, self).__init__()
        self.setupUi(self)
        
        
        self.client = pymongo.MongoClient("mongodb+srv://sumeyra:1234@cluster0.rvan9sx.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["weather_app"]
        self.collection = self.db["weather_infos"]
        self.city_germany = self.db["germany"]
        self.city_america = self.db["america"]
        self.city_netherland = self.db["netherland"]
    
        self.table_cities.cellClicked.connect(self.get_weather)
        self.comboBox_country.currentTextChanged.connect(self.get_cities)
        self.table_cities.itemSelectionChanged.connect(self.get_city_info_germany)
        self.table_cities.itemSelectionChanged.connect(self.get_city_info_netherland)
        self.table_cities.itemSelectionChanged.connect(self.get_city_info_usa)
        
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
        if len(selected_items) == 0:   #If there is no selected item, the function terminates with return.
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
        if len(selected_items) == 0:   #If there is no selected item, the function terminates with return.
            return
        
        selected_city = selected_items[0].text()
        query = {"country": "USA", "city": selected_city}
        city_info = self.city_america.find_one(query)
        if not city_info:
            return

        self.label_country_info.setText("USA")
        self.label_region_info.setText(city_info["region"])
        self.label_population_info.setText(str(city_info["population"]))    
        

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
    
