
    # insert population to population_collection
    population = d['population']
    population_collection.insert_one({'city': city, 'population': population}) 