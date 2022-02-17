# -*- coding: utf-8 -*-
import numpy as np
import requests
import urllib.request
from time import time
from tqdm import tqdm
import json
import pandas as pd
import os.path
import dask
from dask.diagnostics import ProgressBar
ProgressBar().register()

def get_card(card):
    card = card.replace(" ","_")
    url = 'https://api.scryfall.com/cards/named?exact=' + card
    r = requests.get(url = url)
    dic = dict(r.json())
    return dic

start = time()
data = []

with open('PioneerCards.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
  
keys = data.keys()
p = []

lazy_results = []

for card in tqdm(keys):
    task = dask.delayed(get_card)(card)
    lazy_results.append(task)
    # p.append(get_card(card))

results = dask.compute(*lazy_results)

print("\n")
print("\n")
time() - start

info = ["name", "cmc", "legalities", "reprint", "set", "set_type", "rarity", "prices"]
card_info = []
for cards in tqdm(results):
  temp = []
  for k in info:
    if k == "legalities":
      temp.append(cards[k]["pioneer"])
    elif k == "prices":
      temp.append(cards[k]["usd"])
    else:
      temp.append(cards[k])
  card_info.append(temp)

df_cards = pd.DataFrame(card_info,columns=info)

if os.path.isfile('card_list.csv'):
  df_cards.to_csv('card_list.csv', mode='a', header=False)
else:
  df_cards.to_csv('card_list.csv', mode='a', header=True)