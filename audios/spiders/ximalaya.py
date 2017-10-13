# -*- coding: utf-8 -*-
from scrapy import Request, Spider, Selector
import json
from audios.items import XimalayaItem


class XimalayaSpider(Spider):
    name = 'ximalaya'
    allowed_domains = ['www.ximalaya.com']
    start_urls = [
        'http://www.ximalaya.com/52873641/index_tracks?page={page}',
        'http://www.ximalaya.com/32811238/index_tracks?page={page}',
        'http://www.ximalaya.com/15151855/index_tracks?page={page}',
        'http://www.ximalaya.com/63920164/index_tracks?page={page}',
        'http://www.ximalaya.com/38521410/index_tracks?page={page}',
        'http://www.ximalaya.com/85653449/index_tracks?page={page}',
        'http://www.ximalaya.com/36080114/index_tracks?page={page}',
        'http://www.ximalaya.com/60120648/index_tracks?page={page}',
        'http://www.ximalaya.com/69577618/index_tracks?page={page}',
        'http://www.ximalaya.com/57262114/index_tracks?page={page}',
        'http://www.ximalaya.com/17554777/index_tracks?page={page}',
        'http://www.ximalaya.com/44456904/index_tracks?page={page}'
    ]
    json_url = 'http://www.ximalaya.com/tracks/{id}.json'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.ximalaya.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    }
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'audios.pipelines.XimalayaPipeline': 300,
        }
    }
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url.format(page=1), headers=self.headers, callback=self.parse_index, meta={'url': url})
    
    def parse_index(self, response):
        data = json.loads(response.text)
        html = data.get('html')
        selector = Selector(text=html)
        ids = selector.xpath('//ul[contains(@class, "body_list")]/@sound_ids').extract_first().split(',')
        for id in ids:
            yield Request(self.json_url.format(id=id), callback=self.parse_json)
        next_page = selector.xpath('//a[contains(., "下一页")]/@data-page').extract_first()
        if next_page:
            next_url = response.meta.get('url').format(page=next_page)
            yield Request(next_url, callback=self.parse_index, meta={'url': response.meta.get('url')})
    
    def parse_json(self, response):
        data = json.loads(response.text)
        item = XimalayaItem()
        item['album'] = data.get('album_title')
        item['title'] = data.get('title')
        item['user'] = data.get('nickname')
        item['file'] = data.get('play_path')
        item['website'] = '喜马拉雅FM'
        yield item
