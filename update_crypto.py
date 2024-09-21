import requests
import gspread
from datetime import datetime
from google.oauth2 import service_account
import pandas as pd
from mysql.connector import connection

data_list = []
data_to_database = []
date = datetime.now().strftime('%d/%m/%Y')

# Connection with Google Spreadsheet
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Connection with local MySQL database using non-real credentials
try:
    conn = connection.MySQLConnection(
        host = "localhost", #127.0.0.1
        user = "root",
        password = "root",
        database = "database"
    )
except Exception as e:
    print(e)

worksheet = client.open("sheet_name").worksheet("label_name")
tokens = worksheet.col_values(1)
filtered_tokens = [token for token in tokens if token not in ['NonToken', 'NonToken2']]

for token in filtered_tokens:
    url = f"https://www.binance.com/api/v3/ticker/24hr?symbol={token}USDT"
    response = requests.get(url).json()
    price = round(float(response['lastPrice']), 2)
    data = {
        'Token': token,
        'Date': date,
        'Price': price
    }
    data_list.append(data)
    data_to_database.append((token, date, price))

worksheet = client.open("sheet_name").worksheet("label_name")
worksheet.clear()

df = pd.DataFrame(data_list)
data_to_update = [df.columns.values.tolist()] + df.values.tolist()
worksheet.update(data_to_update)

if conn.is_connected():
    try: 
        with conn.cursor() as cursor:
            query_insert = """
                INSERT INTO historical_data (`Token`, `Date`, `Price`)
                VALUES (%s, %s, %s)
            """
            cursor.executemany(query_insert, data_to_database)
            conn.commit()
            result = cursor.execute("""SELECT * FROM historical_data""")
            rows = cursor.fetchall()

            worksheet = client.open("sheet_name").worksheet("label_name")
            worksheet.clear()
            
            df = pd.DataFrame(rows)
            data_to_update = [['Token', 'Date', 'Price']] + df.values.tolist()
            worksheet.update(data_to_update)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
else:
    print("Could not connect")
