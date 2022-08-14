from datetime import datetime
import json
from collections import defaultdict
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def actualizarPrecios():
    numero = 1
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    client = gspread.authorize(creds)
    data = requests.get("https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true").json()['data']
    crypto = defaultdict(dict)
    for value in data:
        if value['s'].endswith("BUSD"):
            crypto[value['b']] = {"CURRENT": value['c']}
    with open("out.json", "w") as f:
        f.write(json.dumps(crypto)) #Genera un JSON con la clave y el precio de todas las cryptomonedas
    with open('out.json') as file:
        data = json.load(file) #Carga el JSON para que podamos consultar sus datos
    worksheet = client.open('Archivo').worksheet("Pestaña") #Editar con nombre del archivo y nombre de la pestaña
    monedas = worksheet.col_values(1) #Obtiene todas las claves de los tokens del sheet
    monedas = set(monedas) #Elimina duplicados
    monedas = list(monedas)
    monedas.sort() #Ordena la lista
    datosALimpiar = ['',' ','Token']
    for moneda in monedas:
        for dato in datosALimpiar:
            if dato == moneda:
                try:
                    monedas.remove(dato)
                except:
                    continue
    worksheet = client.open('Archivo').worksheet("Pestaña") #Editar con nombre del archivo y nombre de la pestaña
    for moneda in monedas:
        try:
            worksheet.update_acell('A'+str(numero),moneda)
            worksheet.update_acell('B'+str(numero),data[moneda].get('CURRENT','Error al obtener el precio'))
            numero += 1
        except:
            worksheet.update_acell('B'+str(numero),'La moneda no se encuentra, indicar precio manualmente')
            numero += 1


actualizarPrecios()
print('Se actualizó la planilla a las',datetime.now().strftime('%H:%M'))