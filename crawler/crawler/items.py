# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    wanted_job_card_titles = scrapy.Field()
    wanted_job_card_companys = scrapy.Field()
    wanted_job_card_hrefs = scrapy.Field()
    wanted_detail_tag = scrapy.Field()
    wanted_detail_intro = scrapy.Field()
    wanted_detail_main_work = scrapy.Field()
    wanted_detail_require = scrapy.Field()
    wanted_detail_prefer = scrapy.Field()
    wanted_detail_welfare = scrapy.Field()
    wanted_detail_addr = scrapy.Field()
    
    pass
