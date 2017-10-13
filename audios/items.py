# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class XimalayaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    album = Field()
    user = Field()
    file = Field()
    website = Field()
