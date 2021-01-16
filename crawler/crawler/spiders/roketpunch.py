import scrapy
from scrapy.selector import Selector
from crawler.items import CrawlerItem

class RoketpunchSpider(scrapy.Spider):
    name = 'roketpunch'
    main_url = 'https://www.rocketpunch.com'
    custom_settings= {
        'DOWNLOADER_MIDDLEWARES': { 
            'crawler.middlewares.SeleniumMiddleware': 100 
        }
    }

    def start_requests(self):
        yield scrapy.Request(url=self.main_url+'/jobs?job=1&page=1/',callback=self.parse_main_page)
    
    def parse_main_page(self, response):
        # print(response.text)
        print('-'*10,'크롤링 결과','-'*10)
        last_page_number = int(response.css('#search-results > div.ui.blank.right.floated.segment > div > div.tablet.computer.large.screen.widescreen.only > a:nth-child(7)::text').getall()[0])
        print(last_page_number)
        print('-'*33)
        for page_number in range(1,last_page_number+1) :
            yield scrapy.Request(url =self.main_url+f'/jobs?job=1&page={page_number}',callback=self.parse_number_page)
            
    def parse_number_page(self, response) :
        job_cards = response.css('#company-list > div > div.content').getall()
        for job_card in job_cards :
            job_card_company = Selector(text=job_card).css('div.company-name > a > h4 > strong::text').get()
            job_card_titles = Selector(text=job_card).css('div.company-jobs-detail > div > div > a.nowrap.job-title.primary.link::text').getall()
            job_card_hrefs = Selector(text=job_card).css('div.company-jobs-detail > div > div > a.nowrap.job-title.primary.link::attr(href)').getall()
            
            for index,job_card_href in enumerate(job_card_hrefs) :
                print('')
                yield scrapy.Request(url=self.main_url+job_card_href,callback=self.parse_job_detail,meta={'job_card_title':job_card_titles[index],
                                                                                                    'job_card_company':job_card_company,
                                                                                                    'job_card_href':self.main_url+job_card_href}) 
            #     break
            # break
            
    def parse_job_detail(self, response) :
        doc = CrawlerItem()
        print(response.meta['job_card_title'],response.meta['job_card_company'])
        detail_tag = response.css('#wrap > div.eight.wide.job-content.column > section > div.job-specialties > a::text').getall()
        detail_intro = None#response.css('').getall()
        detail_main_work = response.css('#wrap > div.eight.wide.job-content.column > section > div.duty.break > span ::text').getall()
        detail_require = response.css('#wrap > div.eight.wide.job-content.column > section > div.content.break > span ::text').getall()
        #wrap > div.eight.wide.job-content.column > section:nth-child(8) > div > span
        detail_prefer = None#response.css('').getall()
        detail_welfare = []
        welfare_items = response.css('#wrap > div.eight.wide.job-content.column > section > div > div > div.item').getall()
        for welfare_item in welfare_items :
            welfare_title = Selector(text=welfare_item).css('div.title > span::text').get()
            welfare_text = Selector(text=welfare_item).css('div.content > span::text').getall()
            detail_welfare.append(welfare_title+' : '+','.join(welfare_text))
        detail_addr = response.css('#wrap > div.eight.wide.job-content.column > section > div.office.item > span.address::text').getall()

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
        print('-'*10,'크롤링 결과','-'*10)
        
        yield doc