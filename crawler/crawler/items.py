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

class JobplanetItem(scrapy.Item) :
    # 잡플래닛 검색 데이터 저장
    company_sector = scrapy.Field()
    company_scale = scrapy.Field()
    company_employees = scrapy.Field()
    company_establishment_date = scrapy.Field()
    
    review_count = scrapy.Field()
    star_score = scrapy.Field()
    
    salary_count = scrapy.Field()
    salary_avg = scrapy.Field()
    
    interview_count = scrapy.Field()
    interview_level = scrapy.Field()
    interview_feel = scrapy.Field()
        
    pass