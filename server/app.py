# from flask import Flask, jsonify
# import requests
# from bs4 import BeautifulSoup
# from pymongo import MongoClient
# import datetime
# from flask_cors import CORS
# from dotenv import dotenv_values  

# app = Flask(__name__)
# CORS(app)

# # Load environment variables from .env file
# env_variables = dotenv_values('.env')

# # MongoDB Atlas setup
# client = MongoClient(env_variables['MONGODB_URI'])
# db = client['dam_data']
# collection = db['water_levels']

# def parse_date_from_header(soup):
#     header = soup.find('header', {'class': 'rhead'})
#     if header:
#         date_str = header.find('h3').text.strip()
#         # Extract the date from the string, assuming a format like "MORBE DAM - Actuals as on - 08 July 2024"
#         parts = date_str.split('-')
#         if len(parts) > 1:
#             date_part = parts[-1].strip()  # Extract the last part which is the date
#             try:
#                 date_obj = datetime.datetime.strptime(date_part, '%d %B %Y')
#                 return date_obj.strftime('%Y-%m-%d')
#             except ValueError:
#                 return None
#     return None

# @app.route('/scrape', methods=['GET'])
# def scrape_data():
#     try:
#         url = 'https://www.nmmc.gov.in/navimumbai/morbe-dam1540389919'
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Parse date from header
#         scrape_date = parse_date_from_header(soup)
#         if not scrape_date:
#             return jsonify({'error': 'Failed to parse date from header'}), 500

#         # Extract table data
#         table = soup.find('table', {'class': 'table table-bordered'})
#         rows = table.find_all('tr')

#         # Parse the table rows
#         data = {}
#         for row in rows[1:]:  # Skip the header row
#             cols = row.find_all('td')
#             description = cols[1].text.strip()
#             value_str = cols[2].text.strip()
            
#             # Convert value_str to numeric if applicable
#             try:
#                 value = float(value_str.split()[0])  # Extract numeric part, assuming format like "123 mm"
#             except ValueError:
#                 value = None  # Handle cases where conversion fails
            
#             data[description] = value

#         # Prepare data for MongoDB
#         today_data = {
#             'date': scrape_date,
#             'todays_rainfall': data.get('Todays Rainfall'),
#             'upto_date_rainfall': data.get('Upto Date Rainfall'),
#             'full_supply_level': data.get('Full Supply Level of Dam'),
#             'todays_dam_level': data.get('Todays Dam Level'),
#             'gross_storage': data.get('Gross Storage Storage of Dam'),
#             'todays_gross_storage': data.get('Todays Gross Storage of Dam')
#         }

#         # Check if data for today already exists
#         if collection.find_one({'date': scrape_date}):
#             return jsonify({'message': 'Data for today already exists.'})

#         # Insert data into MongoDB
#         collection.insert_one(today_data)

#         return jsonify(today_data)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/data', methods=['GET'])
# def get_data():
#     try:
#         data = list(collection.find({}, {'_id': 0}).sort('date', -1).limit(5))  # Get the latest 5 entries
#         data.reverse()  # Reverse the list to show the latest entries last
#         return jsonify(data)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
from flask_cors import CORS
from dotenv import dotenv_values

app = Flask(__name__)
CORS(app)

# MongoDB Atlas setup
env_variables = dotenv_values('.env')
client = MongoClient('mongodb+srv://gaurangraorane:gaurangrao@cluster0.uisyhtp.mongodb.net/dam_data?retryWrites=true&w=majority&appName=Cluster0')
db = client['dam_data']
collection = db['water_levels']

def parse_date_from_header(soup):
    header = soup.find('header', {'class': 'rhead'})
    if header:
        date_str = header.find('h3').text.strip()
        parts = date_str.split('-')
        if len(parts) > 1:
            date_part = parts[-1].strip()
            try:
                date_obj = datetime.datetime.strptime(date_part, '%d %B %Y')
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                return None
    return None

@app.route('/scrape', methods=['GET'])
def scrape_data():
    try:
        url = 'https://www.nmmc.gov.in/navimumbai/morbe-dam1540389919'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        scrape_date = parse_date_from_header(soup)
        if not scrape_date:
            return jsonify({'error': 'Failed to parse date from header'}), 500

        existing_data = collection.find_one({'date': scrape_date})
        if existing_data:
            return jsonify({'message': 'Data for today already exists'}), 200

        table = soup.find('table', {'class': 'table table-bordered'})
        rows = table.find_all('tr')

        data = {}
        for row in rows[1:]:
            cols = row.find_all('td')
            description = cols[1].text.strip()
            if description == 'Todays Gross Storage of Dam':
                value = cols[2].text.strip()
            else:
                value = cols[2].text.strip()  # Or fetch numeric value as needed
            # value_str = cols[2].text.strip()
            try:
                value = float(value.split()[0])
            except ValueError:
                value = None
            data[description] = value

        today_data = {
            'date': scrape_date,
            'rainfall (in MM)': data.get('Todays Rainfall'),
            'upto_date_rainfall (in MM)': data.get('Upto Date Rainfall'),
            'full_supply_level': data.get('Full Supply Level of Dam'),
            'todays_dam_level': data.get('Todays Dam Level'),
            'gross_storage': data.get('Gross Storage Storage of Dam'),
            'todays_gross_storage': data.get('Todays Gross Storage of Dam')
        }

        collection.insert_one(today_data)

        return jsonify(today_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        data = list(collection.find({}, {'_id': 0}).sort('date', -1))
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
