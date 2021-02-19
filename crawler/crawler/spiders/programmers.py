import scrapy
from crawler.items import CrawlerItem
from crawler.data_controller import remove_blank_all,wave_split

class ProgrammersSpider(scrapy.Spider):
    name = 'programmers'
    main_url = 'https://programmers.co.kr'
    
    
    def table2dict(self,labels,contents) :
        table_dict = dict()
        if '주요 서비스' in labels :
           del contents[labels.index('주요 서비스')]
        for index,key in enumerate(labels) :
            if key == '경력' :
                if contents[index] in ['신입','경력무관'] or contents[index].split(' ~ ')[0] == '0' :
                    table_dict['신입여부'] = 1
                    table_dict['경력여부'] = '무관'
                else :
                    table_dict['신입여부'] = 0
                    table_dict['경력여부'] = wave_split(contents[index],'년')
            elif key == '연봉' :
                table_dict['연봉'] = wave_split(contents[index],'만원')
            else :
                table_dict[key] = contents[index]
        
        if '연봉' not in labels :
            table_dict['연봉'] = None
        if '직무' not in labels :
            table_dict['직무'] = None
        return table_dict
    
    def start_requests(self):
        yield scrapy.Request(url=self.main_url+'/job?job_position%5Bdummy%5D=0&amp;order=recent&amp;_=1610273854107',
                             callback=self.parse_main_page)
        
    def parse_main_page(self, response):
        print('-'*10,'크롤링 결과','-'*10)
        last_page_number = int(response.css('#paginate > nav > ul > li:nth-child(8) > a::text').getall()[0])
        print(last_page_number)
        print('-'*33)
        #paginate > nav > ul > li:nth-child(8) > a
        for page_number in range(1,last_page_number+1) :
            yield scrapy.Request(url =self.main_url+f'/job?_=1610273854107&job_position%5Bdummy%5D=0&order=recent&page={page_number}',
                                 callback=self.parse_number_page)

    def parse_number_page(self, response) :
        job_card_titles = response.css('#list-positions-wrapper > ul > li > div.item-body > h5 > a::text').getall()
        job_card_companys = response.css('#list-positions-wrapper > ul > li > div.item-body > h6::text').getall()
        job_card_hrefs = response.css('#list-positions-wrapper > ul > li > div.item-body > h5 > a::attr(href)').getall()
        
        for index,job_card_href in enumerate(job_card_hrefs) :
            yield scrapy.Request(url=self.main_url+job_card_href,
                                 callback=self.parse_detail,
                                 meta={'job_card_title':job_card_titles[index],
                                       'job_card_company':remove_blank_all(job_card_companys[index]),
                                       'job_card_href':self.main_url+job_card_href})
        
    def parse_detail(self, response) :
        doc = CrawlerItem()
        print(response.meta['job_card_title'],response.meta['job_card_company'])
        detail_tag = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                    > section.section-stacks > table > tbody > tr > td > code::text').getall()
        detail_position = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                    > section.section-position ').getall()
        detail_requirements = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8\
                                    > section.section-requirements ').getall()
        detail_preference = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                    > section.section-preference ').getall()
        detail_description = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8\
                                    > section.section-description ').getall()
        
        
        table_label = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                    > section.section-summary > table > tbody > tr > td.t-label::text').getall() 
        table_text = response.css('body > div.main > div.position-show > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 \
                                    > section.section-summary > table > tbody > tr > td.t-content::text').getall()
        
        image = response.css('body > div.main > div.position-show > div > div > div.content-side.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-4\
                                > section:nth-child(2) > a > img::attr(src)').get()
        
        table_dict = self.table2dict(table_label,table_text)
        
        # doc 선언
        doc['platform'] = self.name
        
        doc['job_item_logo'] = image
        doc['job_item_title'] = response.meta['job_card_title']
        doc['job_item_href'] = response.meta['job_card_href']
        
        doc['job_item_main_text'] = ''.join(detail_position+detail_requirements+detail_preference+detail_description)
        doc['job_item_salary'] = table_dict['연봉']
        doc['job_item_skill_tag'] = detail_tag
        doc['job_item_sector'] = table_dict['직무']
        doc['job_item_newbie'] = table_dict['신입여부']
        doc['job_item_career'] = table_dict['경력여부']
        doc['job_item_deadline'] = table_dict['기간']
        
        doc['company_name'] = response.meta['job_card_company']
        doc['company_address'] = table_dict['위치']
        
        yield doc