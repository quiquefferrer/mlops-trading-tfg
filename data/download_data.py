import os

# Verificar si existe la carpeta
print("Existe data/raw?:", os.path.exists("data/raw"))
print("Archivos en data/raw:", os.listdir("data/raw") if os.path.exists("data/raw") else "No existe")

# Ejecutar descarga manual
import yfinance as yf
import pandas as pd

# Descargar AAPL directamente
df = yf.download("AAPL", period="max", progress=False, auto_adjust=True)
print("Datos descargados directamente:", len(df))
print("Columnas:", df.columns.tolist())

# Guardar manualmente
df = df.reset_index()
df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
df.to_csv("data/raw/AAPL.csv", index=False)
print("Guardado. Dias:", len(df))
print(df.head())

