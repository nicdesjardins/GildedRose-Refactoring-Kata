# -*- coding: utf-8 -*-

class GildedRose(object):    

    SULFURAS = "Sulfuras, Hand of Ragnaros"
    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"

    MAXIMUM_QUALITY = 50
    
    def __init__(self, items):
        self.items = items
        self.correctCapInitialQualities()

    def correctCapInitialQualities(self):
        for item in self.items:
            if item.quality > self.MAXIMUM_QUALITY:
                item.quality = self.MAXIMUM_QUALITY

    def nextDay(self):
        self.update_quality()
    
    def update_quality(self):
        for item in self.items:
            
            if item.name != self.SULFURAS:
                item.sell_in = item.sell_in - 1
            
            if item.name != self.AGED_BRIE and item.name != self.BACKSTAGE_PASSES:
                if item.quality > 0:
                    if item.name != self.SULFURAS:
                        item.quality = item.quality - 1
            else:
                if item.quality < self.MAXIMUM_QUALITY:
                    item.quality = item.quality + 1
                    if item.name == self.BACKSTAGE_PASSES:
                        if item.sell_in < 11:
                            if item.quality < self.MAXIMUM_QUALITY:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < self.MAXIMUM_QUALITY:
                                item.quality = item.quality + 1
            
            if item.sell_in < 0:
                if item.name != self.AGED_BRIE:
                    if item.name != self.BACKSTAGE_PASSES:
                        if item.quality > 0:
                            if item.name != self.SULFURAS:
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < self.MAXIMUM_QUALITY:
                        item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return self.___str___

    def __str__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
