# -*- coding: utf-8 -*-
from scrapy import Request, Spider
import json

from audios.items import QingtingItem


class QingtingSpider(Spider):
    name = 'qingting'
    allowed_domains = ['www.qingting.fm', 'i.qingting.fm']
    start_ids = ['206314', '222994', '222993', '143128', '220530', '142452', '216854', '154780', '200484', '228437',
                 '221283', '216128', '227544', '219684', '208797', '224935', '224191', '224074', '227846', '220016',
                 '210951']
    
    album_url = 'http://i.qingting.fm/wapi/channels/{id}'
    list_url = 'http://i.qingting.fm/wapi/channels/{id}/programs/page/{page}/pagesize/{pagesize}'
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'audios.pipelines.QingtingPipeline': 300,
        }
    }
    
    def start_requests(self):
        for id in self.start_ids:
            yield Request(self.album_url.format(id=id), callback=self.parse_index, meta={'id': id})
    
    def parse_index(self, response):
        id = response.meta.get('id')
        data = json.loads(response.text)
        album = data.get('data').get('name')
        yield Request(self.list_url.format(id=id, page=1, pagesize=10), callback=self.parse_list,
                      meta={'id': id, 'page': 1, 'album': album})
    
    def parse_list(self, response):
        id = response.meta.get('id')
        page = response.meta.get('page')
        album = response.meta.get('album')
        data = json.loads(response.text)
        for item in data.get('data'):
            yield QingtingItem({
                'title': item.get('name'),
                'album': album,
                'file': 'http://od.qingting.fm/' + item.get('file_path'),
                'website': '蜻蜓FM'
            })
        total = data.get('total')
        if page * 10 < total:
            yield Request(self.list_url.format(id=id, page=page + 1, pagesize=10), callback=self.parse_list,
                          meta={'id': id, 'page': page + 1, 'album': album})
