import requests
import pandas as pd
import time


data = pd.DataFrame(requests.get(url=f'https://api.parrapi.com/api/atlas/products?key=6e85bc2cb31f46f6a282d064f7d2bdec&delta=2020-06-01').json())
print(data['products'])


