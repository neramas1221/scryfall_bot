# -*- coding: utf-8 -*-
import numpy as np
import requests
import urllib.request
from time import time
from tqdm import tqdm
import json
import pandas as pd
import os.path

def get_image(card):
    card = card.replace(" ","_")
    url = 'https://api.scryfall.com/cards/named?exact=' + card
    r = requests.get(url = url)
    dic = dict(r.json())
    return dic

start = time()
data = []

with open('PioneerCards.json') as json_file:
    data = json.load(json_file)
  
keys = data.keys()
p = []
for card in tqdm(keys):
    p.append(get_image(card))

print("\n")
print("\n")
time() - start

info = ["name", "cmc", "legalities", "reprint", "set", "set_type", "rarity", "prices"]
card_info = []
for cards in tqdm(p):
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