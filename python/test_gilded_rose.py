# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

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
    
    def testThatQualityNeverGoesBelowZero(self):
        items = [Item("an item", 0, 0)]
        gilden_rose = GildedRose(items)
        gilden_rose.nextDay()
        self.assertEqual(0, items[0].quality)

class GildedRoseBackStagePassTest(unittest.TestCase):

    def testThatBackStagePassesQualityIncreasesBy1AtMoreThan10DaysLeft(self):
        items = [Item(GildedRose.BACKSTAGE_PASSES, 12, 25)]
        gilden_rose = GildedRose(items)
        gilden_rose.nextDay()
        self.assertEqual(26, items[0].quality)
    
    def testThatBackStagePassesQualityIncreasesBy2AtLessThanOrEq10DaysLeft(self):
        items = [Item(GildedRose.BACKSTAGE_PASSES, 11, 25)]
        gilden_rose = GildedRose(items)
        gilden_rose.nextDay()
        self.assertEqual(27, items[0].quality)
    
    def testThatBackStagePassesQualityIncreasesBy3AtLessThanOrEq5DaysLeft(self):
        items = [Item(GildedRose.BACKSTAGE_PASSES, 6, 25)]
        gilden_rose = GildedRose(items)
        gilden_rose.nextDay()
        self.assertEqual(28, items[0].quality)
    
    def testThatBackStagePassesQualityDropsToZeroAfterConcert(self):
        items = [Item(GildedRose.BACKSTAGE_PASSES, 1, 10)]
        gilden_rose = GildedRose(items)
        gilden_rose.nextDay()
        self.assertEqual(13, items[0].quality)
        gilden_rose.nextDay()
        self.assertEqual(0, items[0].quality)
        gilden_rose.nextDay()
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


if __name__ == '__main__':
    unittest.main()
