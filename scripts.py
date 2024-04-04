import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import schedule
import time
from datetime import datetime

# Configure the scope of the credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

# Path to credential JSON file
credentials_file = 'keyhostwise.json'

# Authenticate and authorize access
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(credentials)

# Function to obtain current world population data
def get_world_population():
    try:
        # Make a request to the API to obtain world population data.
        response = requests.get('https://restcountries.com/v3.1/all')

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Calculate the world population by summing the population of all countries
            world_population = sum([country['population'] for country in data])
            return world_population
        else:
            print('Error in obtaining world population data:', response.status_code)
            return None
    except Exception as e:
        print('Error in obtaining world population data:', e)
        return None

# Function to update the spreadsheet with the world population and timestamp
def update_sheet():
    try:
        # Open the spreadsheet
        spreadsheet = client.open('HostWise_Script')
        worksheet = spreadsheet.sheet1  # You can change the name of the sheet as needed.

        # Obtain current world population
        world_population = get_world_population()

        if world_population is not None:
            # Get current timestamp
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Get the last row of the spreadsheet
            last_row = len(worksheet.col_values(1)) + 1

            # Update spreadsheet with world population and timestamp
            worksheet.update_cell(last_row, 1, world_population)
            worksheet.update_cell(last_row, 2, current_time)

            print('World Population and Timestamp updated in the spreadsheet:', world_population, current_time)
        else:
            print('The current world population could not be obtained.')
    except Exception as e:
        print('Error updating spreadsheet:', e)

# Schedule the execution of the function to update the spreadsheet every day at 9 a.m.
schedule.every().day.at("09:00").do(update_sheet)

# Keep the script running so that it can perform scheduled updates.
while True:
    schedule.run_pending()
    time.sleep(5)  # Wait X seconds before rechecking for scheduled tasks to be executed.
