import scrapy
from crawler.items import CrawlerItem

class ProgrammersSpider(scrapy.Spider):
    name = 'programmers'
    main_url = 'https://programmers.co.kr'
    
    def start_requests(self):
        yield scrapy.Request(url=self.main_url+'/job?job_position%5Bdummy%5D=0&amp;order=recent&amp;_=1610273854107',callback=self.parse_main_page)
        
    def parse_main_page(self, response):
        print('-'*10,'크롤링 결과','-'*10)
        last_page_number = int(response.css('#paginate > nav > ul > li:nth-child(8) > a::text').getall()[0])
        print(last_page_number)
        print('-'*33)
        #paginate > nav > ul > li:nth-child(8) > a
        for page_number in range(1,last_page_number+1) :
            yield scrapy.Request(url =self.main_url+f'/job?_=1610273854107&job_position%5Bdummy%5D=0&order=recent&page={page_number}',callback=self.parse_number_page)

    def parse_number_page(self, response) :
        job_card_titles = response.css('#list-positions-wrapper > ul > li > div.item-body > h5 > a::text').getall()
        job_card_companys = response.css('#list-positions-wrapper > ul > li > div.item-body > h6::text').getall()
        job_card_hrefs = response.css('#list-positions-wrapper > ul > li > div.item-body > h5 > a::attr(href)').getall()
        
        for index,job_card_href in enumerate(job_card_hrefs) :
            yield scrapy.Request(url=self.main_url+job_card_href,callback=self.parse_detail,meta={'job_card_title':job_card_titles[index],
                                                                                                  'job_card_company':job_card_companys[index],
                                                                                                  'job_card_href':self.main_url+job_card_href})
        
    def parse_detail(self, response) :
        doc = CrawlerItem()
        print(response.meta['job_card_title'],response.meta['job_card_company'])
        detail_tag = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                    > section.section-stacks > table > tbody > tr > td > code::text').getall()
        detail_intro = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                    > section.section-summary > table > tbody > tr > td.t-content::text').getall()
        detail_main_work = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                    > section.section-position > div > div > ul > li::text').getall()
        detail_require = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8\
                                    > section.section-requirements > div > div > ul > li::text').getall()
        detail_prefer = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                    > section.section-preference > div > div > ul > li::text').getall()
        detail_welfare = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8\
                                    > section.section-description > div > div > p::text').getall()
        table_label = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                    > section.section-summary > table > tbody > tr > td.t-label::text').getall()
        detail_addr = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                        > section.section-summary > table > tbody > tr:nth-child({}) > td.t-content::text'.format(table_label.index('위치')+1)).get()
        
        
        doc['job_card_titles'] = response.meta['job_card_title']
        doc['job_card_companys'] = response.meta['job_card_company']
        doc['job_card_hrefs'] = response.meta['job_card_href']
        doc['detail_tag'] = detail_tag
        doc['detail_intro'] = detail_intro
        doc['detail_main_work'] = detail_main_work
        doc['detail_require'] = detail_require
        doc['detail_prefer'] = detail_prefer
        doc['detail_welfare'] = detail_welfare
        doc['detail_addr'] = detail_addr
        doc['platform'] = self.name
        
        yield doc