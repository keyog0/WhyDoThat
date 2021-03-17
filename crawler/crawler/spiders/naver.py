import scrapy
from crawler.items import CrawlerItem
from crawler.data_controller import style_image_parse,control_deadline,control_skill_tag_naver
from datetime import datetime

class NaverSpider(scrapy.Spider):
    name = 'naver'
    main_url = 'https://recruit.navercorp.com'
    custom_settings= {
        'DOWNLOADER_MIDDLEWARES': { 
            'crawler.middlewares.SeleniumMiddleware': 100 
        },
        # 'ITEM_PIPELINES' : {
        #     'crawler.pipelines.CrawlerPipeline': 300
        # }
    }
    start_time = None

    def recognize_newbie(self,title) :
        if '신입' in title or '인턴' in title :
            ret_dict = {'신입여부' : True , '경력여부' : '무관'}
        else :
            ret_dict = {'신입여부' : False , '경력여부' : '2,10'}
        
        return ret_dict

    def start_requests(self):
        yield scrapy.Request(url=self.main_url+'/naver/job/list/developer',callback=self.parse_main_card)
    
    def parse_main_card(self, response):
        # print(response.text)
        job_card_titles = response.css('#jobListDiv > ul > li > a > span > strong::text').getall()
        logo_image = response.css('#jobListDiv > ul > li > a > span > span.crd_ci > img::attr(src)').getall()
        job_card_hrefs = response.css('#jobListDiv > ul > li > a::attr(href)').getall()
        detail_deadline = response.css('#jobListDiv > ul > li > a > span > em::text').getall()

        for index,job_card_href in enumerate(job_card_hrefs) :
            yield scrapy.Request(url=self.main_url+job_card_href,callback=self.parse_job_detail,meta={'job_card_title':job_card_titles[index],
                                                                                                  'logo_image':self.main_url+'/'+logo_image[index],
                                                                                                  'job_card_href':self.main_url+job_card_href,
                                                                                                  'detail_deadline':detail_deadline[index]})

    def parse_job_detail(self, response):
        doc = CrawlerItem()
        print(response.meta['job_card_title'],response.meta['logo_image'])

        if response.meta['detail_deadline'] == '마감' :
            pass
        
        else :
            job_card_companys = response.css('#content > div > div.career_detail > div.dtl_context > div.context_area > div.n_career_header > h1 > span > font::text').get()
            detail_main_text = response.css('#content > div > div.career_detail > div.dtl_context > div.context_area ').getall()
            detail_tag = response.css('#content > div > div.career_detail > div.dtl_context > span > a::text').getall()

            newbie_dict = self.recognize_newbie(response.meta['job_card_title'])

            doc['platform'] = self.name

            doc['logo_image'] = response.meta['logo_image']
            doc['title'] = response.meta['job_card_title']
            doc['href'] = response.meta['job_card_href']
            
            doc['main_text'] = ''.join(detail_main_text).replace("\'",'＇')
            doc['salary'] = None
            doc['skill_tag'] = control_skill_tag_naver(detail_tag)
            doc['sector'] = response.meta['job_card_title']
            doc['newbie'] = newbie_dict['신입여부']
            doc['career'] = newbie_dict['경력여부']
            doc['deadline'] = control_deadline(response.meta['detail_deadline'].split('~')[1])
            
            doc['company_name'] = '네이버'
            doc['company_address'] = '경기 성남시 분당구 불정로 6 (판교)'
            doc['crawl_date'] = str(datetime.now())
            doc['big_company'] = True
            
            yield doc