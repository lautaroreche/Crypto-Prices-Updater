# Cryptocurrency Prices Updater 🚀

This Python script is used to fetch current prices of cryptocurrencies from the Binance API and update a Google Sheets spreadsheet and a local MySQL database.

## Requirements 📋

- Python 3.x
- Python libraries: requests, gspread, pandas, google.oauth2, mysql.connector, datetime
- Google Cloud Platform service account credentials
- MySQL database

## Installation 🔧

1. Clone this repository or download the file `update_crypto.py`.
2. Install dependencies by running the following command in your terminal:

    ```
    pip install requests gspread pandas google.oauth2 mysql.connector datetime
    ```

## Configuration ⚙️

1. Make sure you have a JSON service account credentials file from Google Cloud Platform (`creds.json`).
2. Create a Google Sheets spreadsheet and share it with the email provided in the service account credentials.
3. Open the file `update_crypto.py` and modify the line `client.open(sheet_name).worksheet(label_name)` with the name of your spreadsheet and the corresponding tab.

## Usage 📄

1. Run the Python script `update_crypto.py`.
2. Observe how the prices and variations are updated in your Google Sheets spreadsheet.

Example of table format:

<img width="304" alt="Captura de pantalla 2024-09-21 a la(s) 6 14 58 p  m" src="https://github.com/user-attachments/assets/7e6a46b0-8949-479a-99f5-b16d4e1c4a93">


## Contributions 🎁

Contributions are welcome! If you'd like to improve this script or add new features, feel free to submit a pull request.
