import requests
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, timezone

# Parameters
product_id = 'BTC-USD'
granularity = 60  # 1 minute
end_time = datetime.now(timezone.utc)  
start_time = end_time - timedelta(minutes=10)

# Coinbase API
url = f'https://api.exchange.coinbase.com/products/{product_id}/candles'
params = {
    'start': start_time.isoformat(),
    'end': end_time.isoformat(),
    'granularity': granularity
}

# Fetch data
response = requests.get(url, params=params)

# Check for errors in response
if response.status_code != 200:
    raise Exception(f"Erreur API Coinbase : {response.status_code} - {response.text}")

data = response.json()

# Ensure data is not empty
if not data:
    raise ValueError("Aucune donnée retournée par l'API.")

# Build DataFrame
df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
df.sort_values('time', inplace=True)

# Afficher les 5 dernières lignes
print(df.tail())

########################################################## Export ##############################################################
export_dir = 'data'
os.makedirs(export_dir, exist_ok=True)

# Génère un nom de fichier avec timestamp
timestamp = end_time.strftime('%Y%m%d_%H%M%S')
filename = f'btc_data_{timestamp}.csv'
filepath = os.path.join(export_dir, filename)

# Sauvegarde au format CSV
df.to_csv(filepath, index=False)
print(f"Données sauvegardées dans : {filepath}")
