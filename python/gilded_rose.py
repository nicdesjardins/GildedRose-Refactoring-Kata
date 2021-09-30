# -*- coding: utf-8 -*-

class GildedRose(object):    

    SULFURAS = "Sulfuras, Hand of Ragnaros"
    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes"

    MAXIMUM_QUALITY = 50
    MINIMUM_QUALITY = 0
    BACKSTAGE_PASS_QUALITY_AFTER_SELL_IN_PASSED = 0

    NORMAL_RATE_OF_QUALITY_DECREASE = 1

    itemsThatDontDecreaseSellIn = [SULFURAS]
    SULFURAS_UNCHANGING_VALUE = 80

    itemsThatDontDecreaseInQuality = [
        SULFURAS, 
        AGED_BRIE, 
        BACKSTAGE_PASSES
    ]

    itemQualityIncreaseBySellInRange = {
        BACKSTAGE_PASSES: [
            { 'start': 0, 'end': 5, 'qualityIncrease': 3 },
            { 'start': 6, 'end': 10, 'qualityIncrease': 2 }
        ]
    }

    def __init__(self, items):
        self.items = items
        self.capInitialQualities()
    
    def capInitialQualities(self):
        for item in self.items:
            if(item.name != self.SULFURAS):
                self.capItemQualityToMax(item)
            else:
                item.quality = self.SULFURAS_UNCHANGING_VALUE
    
    def nextDay(self):
        self.update_quality()
    
    def update_quality(self):
        for item in self.items:
            self.updateItemOnNextDay(item)

    def updateItemOnNextDay(self, item):
        self.updateItemSellIn(item)
        self.updateItemQuality(item)

    def updateItemQuality(self, item):

        if(self.itemDecreasesInQuality(item)):
            self.decreaseItemQuality(item)
        else:
            if self.canIncreaseQuality(item):
                self.increaseQuality(item)
        
        if self.sellInHasPassed(item):
            self.adjustItemQualityPassedSellIn(item)
    
    def itemDecreasesInQuality(self, item):
        return (
            not self.itemsThatDontDecreaseInQuality.__contains__(item.name) 
        )
    
    def decreaseItemQuality(self, item):
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
    
    def sellInHasPassed(self, item):
        return item.sell_in < 0

    def adjustItemQualityPassedSellIn(self, item):
        if item.name == self.BACKSTAGE_PASSES:
            item.quality = self.BACKSTAGE_PASS_QUALITY_AFTER_SELL_IN_PASSED

    def updateItemSellIn(self, item):
        if self.itemDecreasesSellIn(item):
            self.decreaseSellIn(item)
    
    def itemDecreasesSellIn(self, item):
        return not self.itemsThatDontDecreaseSellIn.__contains__(item.name)
    
    def decreaseSellIn(self, item):
        item.sell_in = item.sell_in - 1

    def getQualityIncrease(self, item):
        qualityIncrease = 1
        
        if self.itemQualityIncreaseBySellInRange.__contains__(item.name):
            for range in self.itemQualityIncreaseBySellInRange[item.name]:
                if range['start'] <= item.sell_in <= range['end']:
                    qualityIncrease = range['qualityIncrease']
        
        return qualityIncrease
    
    def increaseQuality(self, item):
        item.quality += self.getQualityIncrease(item)
        self.capItemQualityToMax(item)
    
    def isSpecialItem(self, item):
        return (
            self.itemsThatDontDecreaseInQuality.__contains__(item.name)
        )
    
    def canIncreaseQuality(self, item):
        return item.quality < self.MAXIMUM_QUALITY
    
    def hasReachedMinimumQuality(self, item):
        return item.quality <= self.MINIMUM_QUALITY

    def capItemQualityToMax(self, item):
        if item.quality > self.MAXIMUM_QUALITY:
            item.quality = self.MAXIMUM_QUALITY
    

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ConjuredItem(Item):
    isConjured = True
