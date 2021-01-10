# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    platform = scrapy.Field()
    job_card_titles = scrapy.Field()
    job_card_companys = scrapy.Field()
    job_card_hrefs = scrapy.Field()
    detail_tag = scrapy.Field()
    detail_intro = scrapy.Field()
    detail_main_work = scrapy.Field()
    detail_require = scrapy.Field()
    detail_prefer = scrapy.Field()
    detail_welfare = scrapy.Field()
    detail_addr = scrapy.Field()
    
    pass
