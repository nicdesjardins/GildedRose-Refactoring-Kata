# -*- coding: utf-8 -*-
from __future__ import print_function

from gilded_rose import *
from tabulate import tabulate

if __name__ == "__main__":
    items = [
             Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
             Item(name=GildedRose.AGED_BRIE, sell_in=2, quality=0),
             Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
             Item(name=GildedRose.SULFURAS, sell_in=0, quality=50),
             Item(name=GildedRose.SULFURAS, sell_in=-1, quality=81),
             Item(name=GildedRose.BACKSTAGE_PASSES, sell_in=15, quality=20),
             Item(name=GildedRose.BACKSTAGE_PASSES, sell_in=11, quality=20),
             Item(name=GildedRose.BACKSTAGE_PASSES, sell_in=6, quality=20),
             ConjuredItem(name="Conjured Mana Cake", sell_in=3, quality=6),  # <-- :O
                # Item("some item", 0, 0)
            ]

    days = 15
    import sys
    if len(sys.argv) > 1:
        days = int(sys.argv[1]) + 1
    
    gilded_rose = GildedRose(items)

    for day in range(days):
        print("-------- day %s --------" % day)
        table = []
        for item in items:
            table.append([item.name, item.sell_in, item.quality])
        print(tabulate(table, headers=["Item","Sell In", "Quality"], showindex=True))
        print("")
        gilded_rose.nextDay()
