from flask import Flask, render_template, request
import pandas as pd
import pickle
import logging

pd.set_option('display.max_columns', None)
app = Flask(__name__)

list_of_cities = ['Algona', 'Auburn', 'Beaux Arts Village', 'Bellevue',
       'Black Diamond', 'Bothell', 'Burien', 'Carnation', 'Clyde Hill',
       'Covington', 'Des Moines', 'Duvall', 'Enumclaw', 'Fall City',
       'Federal Way', 'Inglewood-Finn Hill', 'Issaquah', 'Kenmore',
       'Kent', 'Kirkland', 'Lake Forest Park', 'Maple Valley', 'Medina',
       'Mercer Island', 'Milton', 'Newcastle', 'Normandy Park',
       'North Bend', 'Pacific', 'Preston', 'Ravensdale', 'Redmond',
       'Renton', 'Sammamish', 'SeaTac', 'Seattle', 'Shoreline',
       'Skykomish', 'Snoqualmie', 'Snoqualmie Pass', 'Tukwila', 'Vashon',
       'Woodinville', 'Yarrow Point']

cities_dict = {city: 0 for city in list_of_cities}

# Load the trained model
with open('trained_model','rb') as file:
    model = pickle.load(file)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_city_value(city):
    global cities_dict
    for c in cities_dict:
        cities_dict[c] = 1 if c == city else 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the form
    input_data = request.form.to_dict()
    logger.info(f"Selected input data: {input_data}")
    city = input_data['city']
    logger.info(f"Selected city: {city}")
    update_city_value(city)

    # Convert input data to DataFrame
    input_df = pd.DataFrame.from_dict(input_data, orient='index').T

    # Insert the binary city list to the DataFrame
    input_df = input_df.reindex(columns=['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'view', 'condition', 'sqft_above', 'sqft_basement', 'yr_built'] + list_of_cities)
    for city in list_of_cities:
        input_df['city_' + city] = cities_dict[city]

    # Drop columns without prefix 'city_'
    input_df.drop(columns=list_of_cities, inplace=True)
    input_df.drop(columns=['city_Algona'], inplace=True)
    logger.info(f"Preprocessed input DataFrame: {input_df}")

    # Make prediction
    prediction = model.predict(input_df)
    formatted_prediction = "%.2f" % prediction[0]
    logger.info(f"Predicted house price: ${formatted_prediction}")
    # Return the prediction
    return render_template('result.html', prediction=formatted_prediction)

if __name__ == '__main__':
    app.run(debug=True)
