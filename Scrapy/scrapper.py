import scrapy
from scrapy import signals
import time
import json
from pydispatch import dispatcher
from pathlib import Path

class CricketSpider(scrapy.Spider):
    name = "wicketnepal"
    start_urls = ['https://wicketnepal.com/']
    result = {}
    counter = 0

    def __init__(self):
        dispatcher.connect(self.spider_closed,signals.spider_closed)



    def parse(self,response):
        for item in response.css("h2.entry-title a::attr(href)"):
            time.sleep(1)

            yield scrapy.Request(url=item.get(), callback=self.parse_next)

    def parse_next(self,response):
        title = response.css("h1.entry-title::text").get()
        category = response.css("span.entry-category a::text").get()
        author = response.css("span.entry-author a::text").get()
        date = response.css("span.entry-date::text").get()
        image = response.css("p img::attr(src)").get()


        self.result[self.counter] = {
            "name" : title,
            "category": category,
            "author": author,
            "date": date,
            "image": image
        }

        self.counter = self.counter + 1
    
    def spider_closed(self,spider):
        with open ("result.json",'w') as fp:
            json.dump(self.result,fp)









