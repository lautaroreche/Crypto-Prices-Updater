# Cryptocurrency Prices Updater 🚀

This Python script is used to fetch current prices and variations of cryptocurrencies from the Binance API and update a Google Sheets spreadsheet.

## Requirements 📋

- Python 3.x
- Python libraries: requests, gspread, pandas, oauth2client
- Google Cloud Platform service account credentials

## Installation 🔧

1. Clone this repository or download the file `update_crypto.py`.
2. Install dependencies by running the following command in your terminal:

    ```
    pip install requests gspread pandas oauth2client
    ```

## Configuration ⚙️

1. Make sure you have a JSON service account credentials file from Google Cloud Platform (`creds.json`).
2. Create a Google Sheets spreadsheet and share it with the email provided in the service account credentials.
3. Open the file `update_crypto.py` and modify the line `client.open(sheet_name).worksheet(label_name)` with the name of your spreadsheet and the corresponding tab.

## Usage 📄

1. Run the Python script `update_crypto.py`.
2. Observe how the prices and variations are updated in your Google Sheets spreadsheet.

Example of table format:

<img width="285" alt="image" src="https://github.com/lautaroreche/ActualizacionCryptomonedas/assets/97992228/efbdad14-589d-483e-b2d0-4bd0478bb328">


## Contributions 🎁

Contributions are welcome! If you'd like to improve this script or add new features, feel free to submit a pull request.
