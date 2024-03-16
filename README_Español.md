# Actualizador de Precios de Criptomonedas

Este script en Python se utiliza para obtener los precios actuales y las variaciones de las criptomonedas desde la API de Binance y actualizar una hoja de cálculo de Google Sheets.

## Requisitos

- Python 3.x
- Librerías Python: requests, gspread, pandas, oauth2client
- Credenciales de servicio de Google Cloud Platform

## Instalación

1. Clona este repositorio o descarga el archivo `update_crypto.py`.
2. Instala las dependencias ejecutando el siguiente comando en tu terminal:

    ```
    pip install requests gspread pandas oauth2client
    ```

## Configuración

1. Asegúrate de tener un archivo JSON de credenciales de servicio de Google Cloud Platform (`creds.json`).
2. Crea una hoja de cálculo de Google y compártela con el correo electrónico proporcionado en las credenciales de servicio.
3. Abre el archivo `update_crypto.py` y modifica la línea `client.open(sheet_name).worksheet(label_name)` con el nombre de tu hoja de cálculo y la pestaña correspondiente.

## Uso

1. Ejecuta el script Python `update_crypto.py`.
2. Observa cómo se actualizan los precios y las variaciones en tu hoja de cálculo de Google Sheets.

## Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar este script o agregar nuevas características, no dudes en enviar una solicitud de extracción.
