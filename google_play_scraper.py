from google_play_scraper import app
import pandas as pd
import requests
from sqlalchemy import create_engine
import os
import urllib.parse

# Database connection settings (use your connection string)
server = <your-server-ip>
database = <database-name>
username = <username>
password = <password>
dsn_name = <dsn_name>
conn_str = f'mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(f"DSN={dsn_name};UID={username};PWD={password};DATABASE={database}")}'
engine = create_engine(conn_str)
# List of package names (app IDs) for the apps you want to retrieve data for
package_names = [
    "com.f1soft.banksmart.siddhartha&hl=en&gl=NP", 
    "com.f1soft.nabilmbank&hl=en&gl=NP",
    "com.nmb.mobile&hl=en&gl=NP",
    "com.hbl.himb&hl=en&gl=NP",
    "com.laxmibank.mobilemoney&hl=en&gl=NP",
    "com.everestbankltd.mbanking&hl=en&gl=NP",
    "com.f1soft.machmobilebanking.activities.main&hl=en&gl=NP",
    "com.f1soft.sanimamobilebanking&hl=en&gl=NP",
    "com.f1soft.kistmobilebanking.activities.main&hl=en&gl=NP",
    "com.f1soft.citizensmobilebanking&hl=en&gl=NP",
    "com.swifttechnology.globalsmart&hl=en&gl=NP",
    "com.f1soft.nicasiamobilebanking&hl=en&gl=NP",
    "com.f1soft.kumarimobilebanking&hl=en&gl=NP",
    "com.f1soft.megafonebank.activities.starter&hl=en&gl=NP",
    "com.sc.mobilebanking.np&hl=en&gl=NP",
    "com.f1soft.primemobilebanking&hl=en&gl=NP",
    "com.f1soft.rastriyabanijyamobilebanking&hl=en&gl=NP",
    "com.f1soft.nepalmobilebanking&hl=en&gl=NP",
    "com.f1soft.banksmart.adbl&hl=en&gl=NP",
    "com.f1soft.sbifonepay.activities&hl=en&gl=NP"
   # Add more package names as needed
]

app_data = []

for package_name in package_names:
    try:
        # Retrieve app details
        app_details = app(package_name)

        # Extract relevant information
        app_name = app_details['title']
        app_reviews = app_details['reviews']
        app_installs = app_details['installs']
        ratings = app_details['ratings']
        score = app_details['score']
        icon = app_details['icon']
        headerImage = app_details['headerImage']
        histogram = app_details['histogram']

        # Create a dictionary to hold app data
        app_dict = {
            'App Name': app_name,
            'Reviews': app_reviews,
            'Installs': app_installs,
            'Ratings': ratings,
            'Score': score,
            'Icon': icon,
            'Header Image': headerImage,
            'Histogram': histogram
        }

        # Add star rating columns
        rating_columns = {}
        for i in range(1, 6):
            rating_columns[f"{i} Star Ratings"] = histogram[i - 1]

        app_dict.update(rating_columns)

        # Append the dictionary to the list
        app_data.append(app_dict)

    except Exception as e:
        print(f"Error retrieving data for {package_name}: {e}")

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(app_data)
df.to_sql('PLAY_MOBBNK_REVIEW', engine, if_exists='replace', index=False)
# Print the DataFrame
df
