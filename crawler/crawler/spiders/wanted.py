import scrapy
from crawler.items import CrawlerItem

class WantedSpider(scrapy.Spider):
    name = 'wanted'
    custom_settings= {
        'DOWNLOADER_MIDDLEWARES': { 
            'crawler.middlewares.SeleniumMiddleware': 100 
        }
    }
    main_url = 'https://www.wanted.co.kr'
    
    def start_requests(self):
        yield scrapy.Request(url=self.main_url+'/wdlist/518?country=kr&job_sort=job.latest_order&years=-1&locations=all',callback=self.parse_main_card)
    
    def parse_main_card(self, response):
        # print(response.text)
        job_card_titles = response.css('#__next > div > div._1yHloYOs_bDD0E-s121Oaa > div._2y4sIVmvSrf6Iy63okz9Qh > div > ul > li > div > a::attr(data-position-name)').getall()
        job_card_companys = response.css('#__next > div > div._1yHloYOs_bDD0E-s121Oaa > div._2y4sIVmvSrf6Iy63okz9Qh > div > ul > li > div > a::attr(data-company-name)').getall()
        job_card_hrefs = response.css('#__next > div > div._1yHloYOs_bDD0E-s121Oaa > div._2y4sIVmvSrf6Iy63okz9Qh > div > ul > li > div > a::attr(href)').getall()

        for index,job_card_href in enumerate(job_card_hrefs) :
            yield scrapy.Request(url=self.main_url+job_card_href,callback=self.parse_job_detail,meta={'job_card_title':job_card_titles[index],
                                                                                                  'job_card_company':job_card_companys[index],
                                                                                                  'job_card_href':self.main_url+job_card_href})
            
    def parse_job_detail(self, response):
        doc = CrawlerItem()
        print(response.meta['job_card_title'],response.meta['job_card_company'])
        detail_tag = response.css('#__next > div > div._37L2cip40tqu3zm3KC4dAa > div._17tolBMfrAeoPmo6I9pA1P > div._1FVm15xN253istI2zLF_Ax\
                                    > div._33u5kCnL62igIXfrIg7Ikl > section.Bfoa2bzuGpxK9ieE1GxhW > div.ObubI7m2AFE5fxlR8Va9t > ul > li > a::text').getall()
        detail_intro = response.css('#__next > div > div._37L2cip40tqu3zm3KC4dAa > div._17tolBMfrAeoPmo6I9pA1P > div._1FVm15xN253istI2zLF_Ax\
                                    > div._33u5kCnL62igIXfrIg7Ikl > div._31EtVNPZ-KwYCXvVZ3927g > section._1LnfhLPc7hiSZaaXxRv11H > p:nth-child(1) > span::text').getall()
        detail_main_work = response.css('#__next > div > div._37L2cip40tqu3zm3KC4dAa > div._17tolBMfrAeoPmo6I9pA1P > div._1FVm15xN253istI2zLF_Ax\
                                    > div._33u5kCnL62igIXfrIg7Ikl > div._31EtVNPZ-KwYCXvVZ3927g > section._1LnfhLPc7hiSZaaXxRv11H > p:nth-child(3) > span::text').getall()
        detail_require = response.css('#__next > div > div._37L2cip40tqu3zm3KC4dAa > div._17tolBMfrAeoPmo6I9pA1P > div._1FVm15xN253istI2zLF_Ax\
                                    > div._33u5kCnL62igIXfrIg7Ikl > div._31EtVNPZ-KwYCXvVZ3927g > section._1LnfhLPc7hiSZaaXxRv11H > p:nth-child(5) > span::text').getall()
        detail_prefer = response.css('#__next > div > div._37L2cip40tqu3zm3KC4dAa > div._17tolBMfrAeoPmo6I9pA1P > div._1FVm15xN253istI2zLF_Ax\
                                    > div._33u5kCnL62igIXfrIg7Ikl > div._31EtVNPZ-KwYCXvVZ3927g > section._1LnfhLPc7hiSZaaXxRv11H > p:nth-child(7) > span::text').getall()
        detail_welfare = response.css('#__next > div > div._37L2cip40tqu3zm3KC4dAa > div._17tolBMfrAeoPmo6I9pA1P > div._1FVm15xN253istI2zLF_Ax\
                                    > div._33u5kCnL62igIXfrIg7Ikl > div._31EtVNPZ-KwYCXvVZ3927g > section._1LnfhLPc7hiSZaaXxRv11H > p:nth-child(9) > span::text').getall()
        detail_addr = response.css('#__next > div > div._37L2cip40tqu3zm3KC4dAa > div._17tolBMfrAeoPmo6I9pA1P > div._1FVm15xN253istI2zLF_Ax\
                                    > div._33u5kCnL62igIXfrIg7Ikl > div._31EtVNPZ-KwYCXvVZ3927g > section._3XP3DBqOgzsz7P6KrVpbGO > div:nth-child(2) > span::text').getall()[1]

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