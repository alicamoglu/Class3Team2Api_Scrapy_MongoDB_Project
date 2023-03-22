import pymongo
from pymongo import MongoClient
import json

# Connect Mongodb
client = MongoClient("mongodb+srv://sumeyra:1234@cluster0.rvan9sx.mongodb.net/?retryWrites=true&w=majority")

# Save USA data
with open('america_city.json') as f:
    data = json.loads(f.read())

db_america = client['america']
regions_collection = db_america['regions']
cities_collection = db_america['cities']
population_collection = db_america['population']

for d in data:
    # insert region to regions_collection
    region = d['region']
    regions_collection.insert_one({'name': region})

    # insert city to cities_collection
    city = d['city']
    cities_collection.insert_one({'name': city, 'region': region})

    # insert population to population_collection
    population = d['population']
    population_collection.insert_one({'city': city, 'population': population})

# Save Germany data
with open('germany_city.json') as f:
    data = json.loads(f.read())

db_germany = client['germany']
regions_collection = db_germany['regions']
cities_collection = db_germany['cities']
population_collection = db_germany['population']

for d in data:
    # insert region to regions_collection
    region = d['region']
    regions_collection.insert_one({'name': region})

    # insert city to cities_collection
    city = d['city']
    cities_collection.insert_one({'name': city, 'region': region})

    # insert population to population_collection
    population = d['population']
    population_collection.insert_one({'city': city, 'population': population})

# Save Netherlands data
with open('netherland_city.json') as f:
    data = json.loads(f.read())

db_netherland = client['netherland']
regions_collection = db_netherland['regions']
cities_collection = db_netherland['cities']
population_collection = db_netherland['population']

for d in data:
    # insert region to regions_collection
    region = d['region']
    regions_collection.insert_one({'name': region})

    # insert city to cities_collection
    city = d['city']
    cities_collection.insert_one({'name': city, 'region': region})

    # insert population to population_collection
    population = d['population']
    population_collection.insert_one({'city': city, 'population': population}) 
