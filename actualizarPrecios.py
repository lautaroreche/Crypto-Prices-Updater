import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd



def actualizarPrecios():
    print('Inicio del script')  

    preciosActuales = []
    variaciones = []
    otrosElementos = ["", "Seguimiento", "USDT", "Token"]

    # Determina APIs de Google y autoriza credenciales
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    client = gspread.authorize(creds)
    
    # Abre la pestaña Datos del Google Worksheet, obtiene las claves de los tokens, elimina duplicados y ordena la lista
    worksheet = client.open('Inv').worksheet("Datos")
    monedasEnTenencia = worksheet.col_values(1)
    monedasASeguir = worksheet.col_values(22)
    monedas = monedasEnTenencia + monedasASeguir
    monedas = list(set(monedas))
    monedas.sort()

    for elemento in otrosElementos:
        # Elimina elementos de la pestaña que no son tokens
        monedas.remove(elemento)

    for moneda in monedas:
        if moneda.isupper():
            # Guarda los valores necesarios de cada token en dos listas si es que está listado en Binance
            par = moneda + "USDT"
            url = f"https://www.binance.com/api/v3/ticker/24hr?symbol={par}"
            response = requests.get(url).json()
            try:
                preciosActuales.append(float(response.get('lastPrice')))
                variaciones.append(float(response.get('priceChangePercent')))
            except:
                preciosActuales.append('N/A')
                variaciones.append('N/A')

    # Genera un DataFrame con los datos de cada token     
    data = {
        'Token': monedas,
        'Precio actual': preciosActuales,
        'Variación 24h': variaciones
    }
    df = pd.DataFrame(data)
    matriz = df.values.tolist()

    # Abre la pestaña Detalle del Google Worksheet y postea la matriz
    worksheet = client.open('Inv').worksheet('Detalle')
    worksheet.update('A2',matriz)

    print('Fin del script')

  

actualizarPrecios()
