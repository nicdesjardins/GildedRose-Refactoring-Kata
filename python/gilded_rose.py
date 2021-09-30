# -*- coding: utf-8 -*-

class GildedRose(object):    

    SULFURAS = "Sulfuras, Hand of Ragnaros"
    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes"

    MAXIMUM_QUALITY = 50
    MINIMUM_QUALITY = 0
    BACKSTAGE_PASS_QUALITY_AFTER_SELL_IN_PASSED = 0

    QUALITY_DECREASE_RATE = 1
    QUALITY_DECREASE_CONJURED_ITEM_MULTIPLIER = 2
    QUALITY_DECREASE_SELLIN_PASSED_MULTIPLIER = 2

    QUALITY_INCREASE_RATE = 1

    SELLIN_DECREASE_RATE = 1
    SELLIN_PASSED_THRESHOLD = 0

    itemsThatDontDecreaseSellIn = [SULFURAS]
    SULFURAS_UNCHANGING_VALUE = 80

    itemsThatDontDecreaseInQuality = [
        SULFURAS, 
        AGED_BRIE, 
        BACKSTAGE_PASSES
    ]

    KEY_RANGE_START = 'start'
    KEY_RANGE_END = 'end'
    KEY_QUALITY_INCREASE = 'qualityIncrease'

    itemQualityIncreaseBySellInRange = {
        BACKSTAGE_PASSES: [
            { KEY_RANGE_START: 0, KEY_RANGE_END: 5, KEY_QUALITY_INCREASE: 3 },
            { KEY_RANGE_START: 6, KEY_RANGE_END: 10, KEY_QUALITY_INCREASE: 2 }
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

    def updateItemSellIn(self, item):
        if self.itemDecreasesSellIn(item):
            self.decreaseSellIn(item)
    
    def itemDecreasesSellIn(self, item):
        return not self.itemsThatDontDecreaseSellIn.__contains__(item.name)
    
    def decreaseSellIn(self, item):
        item.sell_in -= self.SELLIN_DECREASE_RATE
    
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
        item.quality -= self.qualityDecreaseRate(item)
        if item.quality < 0: # quality is never negative
            item.quality = 0
    
    def qualityDecreaseRate(self, item):
        rate = self.QUALITY_DECREASE_RATE
        
        if self.isConjuredItem(item):
            rate *= self.QUALITY_DECREASE_CONJURED_ITEM_MULTIPLIER
        
        if self.sellInHasPassed(item):
            rate *= self.QUALITY_DECREASE_SELLIN_PASSED_MULTIPLIER

        return rate
    
    def isConjuredItem(self, item):
        return isinstance(item, ConjuredItem)
    
    def sellInHasPassed(self, item):
        return item.sell_in < self.SELLIN_PASSED_THRESHOLD

    def adjustItemQualityPassedSellIn(self, item):
        if item.name == self.BACKSTAGE_PASSES:
            item.quality = self.BACKSTAGE_PASS_QUALITY_AFTER_SELL_IN_PASSED

    def getQualityIncrease(self, item):
        qualityIncrease = self.QUALITY_INCREASE_RATE
        
        if self.itemQualityIncreaseBySellInRange.__contains__(item.name):
            for range in self.itemQualityIncreaseBySellInRange[item.name]:
                if range[self.KEY_RANGE_START] <= item.sell_in <= range[self.KEY_RANGE_END]:
                    qualityIncrease = range[self.KEY_QUALITY_INCREASE]
        
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
