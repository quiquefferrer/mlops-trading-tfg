import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

def update_stock_data(ticker="AAPL", days_back=5):
    """
    Actualiza datos de un ticker desde yfinance
    """
    file_path = f"data/raw/{ticker}.csv"
    
    # 1. Cargar datos existentes o crear nuevo
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path, index_col=0)
        df_existing.index = pd.to_datetime(df_existing.index, errors="coerce")
        df_existing = df_existing[~df_existing.index.isna()].sort_index()
        last_date = df_existing.index[-1].date()
    else:
        df_existing = pd.DataFrame()
        last_date = datetime(1980, 1, 1).date()  # Fecha por defecto
    
    # 2. Verificar si necesitamos actualizar
    today = datetime.now().date()
    
    # Si los datos tienen menos de 'days_back' días, actualizar
    if (today - last_date).days > days_back:
        print(f"📥 Actualizando {ticker} (último dato: {last_date})")
        
        # Descargar datos nuevos (desde última fecha + 1 día)
        start_date = last_date + timedelta(days=1)
        new_data = yf.download(ticker, start=start_date, progress=False)
        
        if not new_data.empty:
            # Combinar
            df_updated = pd.concat([df_existing, new_data])
            df_updated = df_updated[~df_updated.index.duplicated(keep='last')]
            
            # Guardar
            df_updated.to_csv(file_path)
            print(f"✅ {ticker} actualizado hasta {df_updated.index[-1].date()}")
            
            # Opcional: Actualizar DVC
            update_dvc(file_path, ticker)
            
            return df_updated
        else:
            print(f"⚠️  No hay datos nuevos para {ticker}")
            return df_existing
    else:
        print(f"✅ {ticker} ya actualizado (hasta {last_date})")
        return df_existing

def update_dvc(file_path, ticker):
    """Actualiza control de versiones con DVC"""
    try:
        import subprocess
        # Añadir a DVC
        subprocess.run(['dvc', 'add', file_path], check=True, capture_output=True)
        # Push a almacenamiento
        subprocess.run(['dvc', 'push'], check=True, capture_output=True)
        
        # Git commit
        subprocess.run(['git', 'add', f'{file_path}.dvc'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Update {ticker}: {datetime.now().date()}'], 
                      check=True)
        subprocess.run(['git', 'push'], check=True)
        print(f"🔄 DVC/Git actualizado para {ticker}")
    except Exception as e:
        print(f"⚠️  Error DVC/Git: {e}")

def update_all_tickers():
    """Actualiza todos los tickers"""
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
    
    for ticker in tickers:
        update_stock_data(ticker)

if __name__ == "__main__":
    # Actualiza solo AAPL para probar
    update_stock_data("AAPL")
    
    # O actualiza todos
    # update_all_tickers()