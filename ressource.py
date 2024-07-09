import requests
from math import floor
from constants import LOCATIONS, PRICE_URL

class Ressource:
    
    def __init__(self, ress_name, num, enchant):
        # 25% royal city craft discount
        self.craft_discount = .25
        
        self.ress_name = ress_name if enchant == 0 and not 'ARTEFACT' in ress_name else ress_name + f'@{enchant}'
        self.num = floor(num * (1 - self.craft_discount)) if not 'ARTEFACT' in ress_name else 1
        self.canCraft = True
        
        self.current_price_response = self._ress_response()
        self._best_price_calc()
        
    def _ress_response(self):
        LOCATIONS_NAMES = ','.join(name for name in LOCATIONS)
        current_price_response = requests.get(PRICE_URL + self.ress_name + '.json?locations=' + LOCATIONS_NAMES + '&qualities=1')
        
        if current_price_response.status_code == 200:
            return current_price_response
        else:
            raise ImportError("Can't import Ress of Item data")
            
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
            
            if not market_prices == 0:
                cities_price.append({'city': city, 'price': market_prices})  
                prices.append(market_prices)
        
        if len(prices) > 0:
            best_price = min(prices)
            self.finding_cityPrice = list(filter(filter_func, cities_price))[0]  
        else:
            self.canCraft = False
        
    @property
    def info(self):
        return {
            'name': f'{self.ress_name}-{self.finding_cityPrice['city']}',
            'Current Price': self.finding_cityPrice['price'] * self.num
        }