# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    platform = scrapy.Field()
    
    job_item_logo = scrapy.Field()
    job_item_title = scrapy.Field()
    job_item_href = scrapy.Field()
    
    job_item_main_text = scrapy.Field()
    job_item_salary = scrapy.Field()
    job_item_skill_tag = scrapy.Field()
    job_item_sector = scrapy.Field()
    job_item_newbie = scrapy.Field()
    job_item_career = scrapy.Field()
    job_item_deadline = scrapy.Field()
    
    company_name = scrapy.Field()
    company_address = scrapy.Field()
    
    detail_intro = scrapy.Field()
    detail_main_work = scrapy.Field()
    detail_require = scrapy.Field()
    detail_prefer = scrapy.Field()
    detail_welfare = scrapy.Field()

class JobplanetItem(scrapy.Item) :
    # 잡플래닛 검색 데이터 저장
    company_name = scrapy.Field()
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
