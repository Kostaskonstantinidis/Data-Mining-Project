from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from areas import cities
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,r2_score


# Initialize Flask app
app = Flask(__name__)

# Function to generate synthetic data
def generate_data(plithos=1000):
    data = {
        'City': [],
        'Area': [],
        'Type': [],
        'Square_meters': [],
        'Orofos': [],
        'Bedrooms': [],
        'Bathrooms': [],
        'Price': [],
        'Furnished': []
    }

    # Generate data for houses
    for city, areas in cities.items():
        for area_info in areas:
            price_range = area_info['price_range']
            for _ in range(plithos // len(cities) // len(areas)):
                data['City'].append(city)
                data['Area'].append(area_info['area'])
                house_type = np.random.choice(['Apartment', 'House', 'Studio'])
                data['Type'].append(house_type)
                if house_type == 'Apartment':
                    data['Square_meters'].append(np.random.randint(50, 201))
                    data['Bedrooms'].append(np.random.randint(1, 5))
                    data['Bathrooms'].append(np.random.randint(1, 3))
                    floor = np.random.choice(range(7), p=[0.025, 0.25, 0.25, 0.25, 0.10, 0.10, 0.025])
                    if floor == 0:
                        if price_range[1] - 200 > price_range[0]:
                            price = np.random.randint(price_range[0], price_range[1] - 200)
                        else:
                            price = price_range[0]
                    else:
                        price = np.random.randint(price_range[0], price_range[1])
                elif house_type == 'House':
                    data['Square_meters'].append(np.random.randint(80, 501))
                    data['Bedrooms'].append(np.random.randint(2, 10))
                    data['Bathrooms'].append(np.random.randint(1, 5))
                    floor = None
                    price = np.random.randint(price_range[0], price_range[1])
                else:  # Studio
                    data['Square_meters'].append(np.random.randint(20, 61))
                    data['Bedrooms'].append(0)
                    data['Bathrooms'].append(1)
                    floor = None
                    price = np.random.randint(price_range[0], price_range[1])

                if house_type == 'Studio':
                    price = int(price / 1.5)
                elif house_type == 'House':
                    price = int(price * 1.5)
                furnished = np.random.choice(['Yes', 'No'])
                data['Furnished'].append(furnished)
                if furnished == 'Yes':
                    price += 100

                data['Price'].append(price)
                data['Orofos'].append(floor)

    return data
