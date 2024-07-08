from item_info import Item
from items import ITEMS_OF_INTEREST

for item in ITEMS_OF_INTEREST:
    ITEM_NAME = item
    
    new_item = Item(ITEM_NAME, '1')
    if not new_item._isStopped:
        print(f'{new_item.info} \n')