import requests
from constants import ITEM_INFO_URL
from ressource import Ressource

class Craft:
    def __init__(self, item_name):
        self.item_name = item_name
        self.item_enchant = 0
        
        self.isCraftable =  True
        
        self.current_item_info_response = self._item_response()
        self._ress_cost_calc()
        
        
    def _item_response(self):
        if '@' in self.item_name:
            self.item_enchant = int(self.item_name[-1])
            self.item_name = self.item_name.split('@')[0]
        current_item_info_response = requests.get(ITEM_INFO_URL + self.item_name + '/data')
       
        if current_item_info_response.status_code == 200:
            return current_item_info_response
        else:
            raise ImportError("Can't import Item Craft data")
        
    def _ress_cost_calc(self):
        self.crafting = {}
        self.totalCost = 0
        
        self.craft_item_info = self.current_item_info_response.json()["craftingRequirements"]["craftResourceList"]
        
        if not self.item_enchant == 0:
            self.craft_item_info = self.current_item_info_response.json()["enchantments"]["enchantments"][self.item_enchant - 1]["craftingRequirements"]["craftResourceList"]
       
        for item in self.craft_item_info:            
            ress_cost = Ressource(item['uniqueName'], item['count'], self.item_enchant)
            if ress_cost.canCraft:
                self.crafting[item['uniqueName']] = ress_cost.info
                self.totalCost += ress_cost.info['Current Price']
            else:
                self.isCraftable = False
        
    @property
    def details(self):
        return {
            'basic': self.craft_item_info,
            'cost': self.crafting,
            'craft-cost': self.totalCost,
        }