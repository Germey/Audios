# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.exceptions import DropItem
from os.path import exists
from os import makedirs
import requests


class XimalayaPipeline():
    def process_item(self, item, spider):
        path = '{website}/{user}/{album}'.format(website=item['website'], user=item['user'], album=item['album'])
        file = '{website}/{user}/{album}/{title}.m4a'.format(website=item['website'], user=item['user'],
                                                             album=item['album'], title=item['title'])
        if not exists(path):
            makedirs(path)
        content = requests.get(item['file']).content
        with open(file, 'wb') as f:
            f.write(content)
        return item


class QingtingPipeline():
    def process_item(self, item, spider):
        path = '{website}/{album}'.format(website=item['website'], album=item['album'])
        file = '{website}/{album}/{title}.m4a'.format(website=item['website'],
                                                      album=item['album'], title=item['title'])
        if not exists(path):
            makedirs(path)
        content = requests.get(item['file']).content
        with open(file, 'wb') as f:
            f.write(content)
        return item
