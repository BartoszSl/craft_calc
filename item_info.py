import requests
from constants import PRICE_URL, LOCATIONS
from item_craft import Craft
import random
    
class Item:
    def __init__(self, item_name, quality):
        
        self.item_name = item_name
        self.quality =  quality
        
        # Important info about Item
        self._isStopped = False
        
        self.current_price_response = self._item_response()
        self._best_price_calc()
        
        itemCraft = Craft(item_name)
        if itemCraft.isCraftable:
            self.craft = itemCraft.details
        else:
            self._isStopped = True
            
    def _item_response(self):
        LOCATIONS_NAMES = ','.join(name for name in LOCATIONS)
        current_price_response = requests.get(PRICE_URL + self.item_name + '.json?locations=' + LOCATIONS_NAMES + '&qualities=' + self.quality)
        
        if current_price_response.status_code == 200:
            return current_price_response
        else:
            raise ImportError("Can't import Item data")
            
    def _best_price_calc(self):
        prices = []
        best_price = 0
        cities_price = []
        
        def filter_func(x):
            if best_price == x['price']:
                return x
            
        for i in range(len(LOCATIONS)):
            market_prices = self.current_price_response.json()[i]['sell_price_min']
            city = self.current_price_response.json()[i]['city']
            
            cities_price.append({'city': city, 'price': market_prices})
            prices.append(market_prices)
        
        best_price = max(prices)
        self.finding_cityPrice = list(filter(filter_func, cities_price))[0]
        
    @property
    def info(self):
        if not self._isStopped:
            return {
                'name': f'{self.item_name}-{self.finding_cityPrice['city']}',
                'Current Price': self.finding_cityPrice['price'],
                'profit': self.finding_cityPrice['price'] - self.craft['craft-cost'],
                'Crafting': self.craft['basic'],
                # 'Crafting-cost': self.craft['cost'],
                # 'Total-craft-cost': self.craft['craft-cost']
            }
        else:
            return {
                'name': f'{self.item_name}',
                'status': "Can't craft"
            }
    