
from scrapy import Spider,Request
from yunyinyue.items import YunyinyueItem
from urllib.parse import quote
from lxml import etree

class YunyinyueSpider(Spider):
    name = 'yunyinyue'

    def start_requests(self):
        singer = '周杰伦'
        raw_url = 'https://www.xiami.com/search/song/page/{}?spm=a1z1s.3521869.0.0.UYlQOM&key={}6&category=-1'
        for i in  range(60):
            url = raw_url.format(str(i+1),quote(singer))
            yield Request(url=url,callback=self.parse)


    def parse(self, response):
        selector = etree.HTML(response.text)
        hrefs = selector.xpath('//td[@class="song_name"]/a[1]/@href')
        titles = selector.xpath('//td[@class="song_name"]/a/text()')

        for href,title in zip(hrefs,titles):
            url = 'https:'+href
            yield Request(url=url, callback=self.parse_content,meta={"title":title})




    def parse_content(self,response):
        selector = etree.HTML(response.text)

        song_list = selector.xpath('//div[@class="lrc_main"]/text()')
        song = []
        for line  in song_list:
            song.append(line.strip())
        result = ','.join(song)#连接字符
        item = YunyinyueItem()
        item['title'] = response.meta['title']
        item['song'] = result
        yield item





