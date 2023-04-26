import json
from collections import defaultdict
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime



def actualizarPrecios():
    crypto1 = defaultdict(dict)
    crypto2 = defaultdict(dict)

    print('------------------------------------------------')  
    print('----- Comenzó la actualización a las',datetime.now().strftime('%H:%M'),'-----')

    numero = 2
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    client = gspread.authorize(creds)

    #Crypto general data
    api1 = requests.get("https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true").json()['data']
    #24hr Ticker Price Change Statistics
    api2 = requests.get("https://www.binance.com/api/v3/ticker/24hr").json()
    
    # Abre la pestaña Datos del Google Worksheet Crypto
    worksheet = client.open('Crypto').worksheet("Datos")
    # Obtiene todas las claves de los tokens del sheet
    monedas = worksheet.col_values(2) 
    # Elimina duplicados
    monedas = list(set(monedas)) 
    # Ordena la lista
    monedas.sort() 

    # Elimina de la lista de monesas lo que nos sean claves de tokens
    for moneda in monedas:
        if moneda.isupper() == False or len(moneda) > 5 or moneda in ['Token','Atento compras','']:
            try:
                monedas.remove(moneda)
            except:
                continue

    # Toma los valores de cada api
    for value in api1:
        if value['s'].endswith("USDT"):
            crypto1[value['b']] = {"CURRENT": value['c']}
    for value in api2:
        if value['symbol'].endswith("USDT"):
            crypto2[value['symbol'][:-4]] = {"RESULTADO24HORAS": value['priceChangePercent'], "MAXIMO24HORAS": value['highPrice'], "MINIMO24HORAS": value['lowPrice']}

    # Genera los json
    with open("api1.json", "w") as api1:
        api1.write(json.dumps(crypto1)) 
    with open("api2.json", "w") as api2:
        api2.write(json.dumps(crypto2))

    # Carga los json para que podamos consultar sus datos
    with open('api1.json') as api1:
        api1 = json.load(api1) 
    with open('api2.json') as api2:
        api2 = json.load(api2)

    worksheet = client.open('Crypto').worksheet("Detalle")

    for moneda in monedas:
        try:
            worksheet.update_acell('A'+str(numero),moneda)
            worksheet.update_acell('B'+str(numero),api1[moneda].get('CURRENT','Error al obtener el precio'))
            worksheet.update_acell('C'+str(numero),api2[moneda].get('RESULTADO24HORAS','Error al obtener el precio'))
            numero += 1
            print('Actualizó ' + moneda + ' ya que la encontró en Binance')
        except:
            worksheet.update_acell('B'+str(numero),'N/A')
            worksheet.update_acell('C'+str(numero),'N/A')
            numero += 1
            print('No se actualizó ' + moneda + ' ya que no la encontró en Binance')
        time.sleep(2)
  
    print('----- Se actualizó la planilla a las',datetime.now().strftime('%H:%M'),'-----')
    print('------------------------------------------------')  


actualizarPrecios()
