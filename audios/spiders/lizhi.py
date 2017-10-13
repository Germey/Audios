# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy_splash import SplashRequest

from audios.items import LizhiItem


class LizhiSpider(Spider):
    name = 'lizhi'
    allowed_domains = ['www.lizhi.fm']
    start_users = ['2502957709533089324', '2600257474804913708', '6092400', '2547367353443086380',
                   '2562056770807676972', '2510105112787701804', '2533601034174041644', '2538999144390726188',
                   '2608789251244364844', '2524771356655725100', '14672638', '2592578799130110508',
                   '2569141252789175852',
                   '5188491', '2610670309481415724', '14085565', '2588313415568750636', '2501378445975017516',
                   '2615388260189478444',
                   '2596351949373314092', '2503604501542412332', '13180386', '321173', '2545666318761474604',
                   '2568555657620952620', '2589490689727826988', '2515774671480881196', '2597381343514776108',
                   '2579617925712374828']
    
    index_url = 'http://www.lizhi.fm/user/{user}'
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'audios.pipelines.LizhiPipeline': 300,
        }
    }
    
    http_user = 'admin'
    http_pass = 'admin'
    
    def start_requests(self):
        for user in self.start_users:
            yield Request(self.index_url.format(user=user), callback=self.parse_index)
    
    def parse_index(self, response):
        user = response.css('h1.user-info-name::text').extract_first()
        items = response.css('ul.audioList.js-audio-list li')
        for item in items:
            title = item.xpath('./a/@data-title').extract_first()
            file = item.xpath('./a/@data-url').extract_first()
            yield LizhiItem({
                'title': title,
                'file': response.urljoin(file),
                'website': '荔枝FM',
                'user': user
            })
        next = response.urljoin(response.css('.page .next::attr(href)').extract_first())
        yield Request(next, callback=self.parse_index)
