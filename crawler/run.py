import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from crawler.spiders.programmers import ProgrammersSpider
from crawler.spiders.roketpunch import RoketpunchSpider
from crawler.spiders.wanted import WantedSpider
# from crawler.spiders.programmmers import ProgrammersSpider
# from crawler.spiders.roketpunch import RoketpunchSpider
# from crawler.spiders.wanted import WantedSpider

configure_logging()
runner = CrawlerRunner()
#runner.crawl(ProgrammersSpider)
runner.crawl(RoketpunchSpider)
#runner.crawl(WantedSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run() # the script will block here until all crawling jobs are finished