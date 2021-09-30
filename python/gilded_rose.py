# -*- coding: utf-8 -*-

class GildedRose(object):    

    SULFURAS = "Sulfuras, Hand of Ragnaros"
    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes"

    MAXIMUM_QUALITY = 50
    MINIMUM_QUALITY = 0
    NORMAL_RATE_OF_QUALITY_DECREASE = 1
    
    itemsThatDontDecreaseSellIn = [SULFURAS]
    SULFURAS_VALUE = 80

    itemsThatDontDecreaseInQuality = [
        SULFURAS, 
        AGED_BRIE, 
        BACKSTAGE_PASSES
    ]

    def __init__(self, items):
        self.items = items
        self.capInitialQualities()

    def nextDay(self):
        self.update_quality()
    
    def update_quality(self):
        
        for item in self.items:
            
            self.updateSellIn(item)
            
            if(self.itemDecreasesInQuality(item)):
                self.decreaseQuality(item)
            else:
                if self.canIncreaseQuality(item):
                    self.increaseQuality(item)
            
            if self.sellInHasPassed(item):
                if item.name == self.BACKSTAGE_PASSES:
                    item.quality = 0

    def updateSellIn(self, item):
        if self.itemDecreasesSellIn(item):
            self.decreaseSellIn(item)

    def increaseQuality(self, item):
        item.quality = item.quality + 1
        if item.name == self.BACKSTAGE_PASSES:
            if item.sell_in < 11:
                if item.quality < self.MAXIMUM_QUALITY:
                    item.quality = item.quality + 1
            if item.sell_in < 6:
                if item.quality < self.MAXIMUM_QUALITY:
                    item.quality = item.quality + 1
    
    def isSpecialItem(self, item):
        return (
            self.itemsThatDontDecreaseInQuality.__contains__(item.name)
        )
    
    def sellInHasPassed(self, item):
        return item.sell_in < 0
    
    def canIncreaseQuality(self, item):
        return item.quality < self.MAXIMUM_QUALITY
    
    def itemDecreasesInQuality(self, item):
        return (
            not self.itemsThatDontDecreaseInQuality.__contains__(item.name) 
        )
    
    def decreaseQuality(self, item):
        item.quality = item.quality - self.qualityDecreaseRate(item)
        if item.quality < 0: # quality is never negative
            item.quality = 0
    
    def qualityDecreaseRate(self, item):
        rate = self.NORMAL_RATE_OF_QUALITY_DECREASE
        
        if self.isConjuredItem(item):
            rate *= 2
        
        if self.sellInHasPassed(item):
            rate *= 2

        return rate
    
    def isConjuredItem(self, item):
        return isinstance(item, ConjuredItem)

    

    def decreaseSellIn(self, item):
        item.sell_in = item.sell_in - 1
    
    def itemDecreasesSellIn(self, item):
        return not self.itemsThatDontDecreaseSellIn.__contains__(item.name)

    

    def hasReachedMinimumQuality(self, item):
        return item.quality <= self.MINIMUM_QUALITY

    def capInitialQualities(self):
        for item in self.items:
            if(item.name != self.SULFURAS):
                if item.quality > self.MAXIMUM_QUALITY:
                    item.quality = self.MAXIMUM_QUALITY
            else:
                item.quality = self.SULFURAS_VALUE

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return self.___str___

    def __str__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class ConjuredItem(Item):
    isConjured = True
