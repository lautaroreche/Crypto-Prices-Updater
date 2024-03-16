import requests
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)


current_prices = []
variations = []
worksheet = client.open(sheet_name).worksheet(label_name)
tokens = list(set(worksheet.col_values(1)))
tokens.sort()

# Delete everything that is not tokens
for token in tokens:
    if token.isupper() == False:
        tokens.remove(token)

for token in tokens:
    url = f"https://www.binance.com/api/v3/ticker/24hr?symbol={token}USDT"
    response = requests.get(url).json()
    try:
        current_prices.append(float(response['lastPrice']))
        variations.append(float(response['priceChangePercent']))
    except:
        current_prices.append('Not listed')
        variations.append('Not listed')

info = {
    'Token': tokens,
    'Current price': current_prices,
    'Variation 24h': variations
}
df = pd.DataFrame(info)
df_list = df.values.tolist()
worksheet.batch_clear(["V2:X"])
worksheet.update('V2', df_list)
