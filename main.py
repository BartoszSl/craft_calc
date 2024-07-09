from item_info import Item
from items import ITEMS_OF_INTEREST

all_info_items = []

for item in ITEMS_OF_INTEREST:
    ITEM_NAME = item
    
    new_item = Item(ITEM_NAME, '1')
    if not new_item._isStopped:
        all_info_items.append(new_item.info)

# Sorted from the biggest to smallest profit 
sorted_items = sorted(all_info_items, key = lambda x: x['profit'], reverse = True)

for item_info in sorted_items:
    print(item_info['name'])
    print(f'Price: {item_info['Current Price']}')
    print(f'Profit: {item_info['profit']}\n')