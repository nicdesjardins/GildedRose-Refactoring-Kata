# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose, ConjuredItem

class GildedRoseNormalItemTest(unittest.TestCase):
    
    def testThatNameIsCorrectlySetAfterUpdateQuality(self):
        items = [Item("foo", 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay() # update_quality()
        self.assertEqual("foo", items[0].name)

    def testThatSellInDateReducesNextDay(self):
        items = [Item("an item", 10, 30)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(9, items[0].sell_in)
    
    def testThatQualityReducesNextDay(self):
        items = [Item("an item", 10, 30)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(29, items[0].quality)

    def testThatQualityOfAnItemIsNeverMoreThanMaximumDefinedQuality(self):
        items = [Item("an item", 10, 999)]
        GildedRose(items)
        self.assertLessEqual(items[0].quality, GildedRose.MAXIMUM_QUALITY)
    
    def testThatQualityOfAnItemIsNeverNegative(self):
        items = [Item("an item", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(0, items[0].quality)
    
    def testThatSellInCanBeLessThanZero(self):
        items = [Item("an item", 0, 5)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertLess(items[0].sell_in, 0)
    
    def testThatNonConjuredItemsAreNotConjured(self):
        items = [Item("non-conjured item", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertFalse(isinstance(items[0], ConjuredItem))

class GildedRoseBackStagePassTest(unittest.TestCase):

    def testThatBackStagePassesQualityIncreasesBy1AtMoreThan10DaysLeft(self):
        items = [Item(GildedRose.BACKSTAGE_PASSES, 12, 25)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(26, items[0].quality)
    
    def testThatBackStagePassesQualityIncreasesBy2AtLessThanOrEq10DaysLeft(self):
        items = [Item(GildedRose.BACKSTAGE_PASSES, 11, 25)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(27, items[0].quality)
    
    def testThatBackStagePassesQualityIncreasesBy3AtLessThanOrEq5DaysLeft(self):
        items = [Item(GildedRose.BACKSTAGE_PASSES, 6, 25)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(28, items[0].quality)
    
    def testThatBackStagePassesQualityDropsToZeroAfterConcert(self):
        items = [Item(GildedRose.BACKSTAGE_PASSES, 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(0, items[0].quality)

class GildedRoseSulfurasTest(unittest.TestCase):
    
    def testThatSulfurasQualityDoesntDecrease(self):
        items = [Item(GildedRose.SULFURAS, 10, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(50, items[0].quality)

    def testThatSulfurasSellInDateDoesntDecrease(self):
        items = [Item(GildedRose.SULFURAS, 10, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(10, items[0].sell_in)

class GildedRoseAgedBrieTest(unittest.TestCase):

    def testThatAgedBrieSellInDateDecreasesNextDay(self):
        items = [Item(GildedRose.AGED_BRIE, 10, 30)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(9, items[0].sell_in)
    
    def testThatAgedBrieQualityIncreasesNextDay(self):
        items = [Item(GildedRose.AGED_BRIE, 10, 30)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertEqual(31, items[0].quality)

class GildedRoseConjuredItemTest(unittest.TestCase):
    
    def testThatConjuredItemsAreConjured(self):
        items = [ConjuredItem("conjured item", 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.nextDay()
        self.assertTrue(isinstance(items[0], ConjuredItem))


if __name__ == '__main__':
    unittest.main()
