# -*- coding: utf-8 -*-
import scrapy, logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jdbspider.items import jobItem
from lxml import etree


class SimplespiderSpider(CrawlSpider):
    name = 'simplespider'
    allowed_domains = ['hk.jobsdb.com']
    start_urls = [
    'https://hk.jobsdb.com/hk/search-jobs/big-data/1',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/2',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/3',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/4',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/5',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/6',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/7',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/8',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/9',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/10',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/11',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/12',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/13',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/14',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/15',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/16',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/17',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/18',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/19',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/20',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/21',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/22',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/23',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/24',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/25',
    'https://hk.jobsdb.com/hk/search-jobs/big-data/26'
    ]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def parse(self, response):
        for job_div in response.xpath("//div[@data-automation='job-title']").getall():
            job = jobItem()
            tree = etree.fromstring(job_div)
            job['title'] = "".join(tree.xpath('//a/span/span//text()'))
            yield response.follow(tree.xpath('//a/@href')[0], callback=self.parse_jobpage, meta={'job': job})

    def parse_jobpage(self, response):
        job = response.meta['job']

        #yield {
        #    'Job Functions': response.xpath("//strong[text()='Job Functions']/parent::span").re(r'\/strong>: (.*)</span>')
        #}

        span_list = response.css("span::text").extract()
        p_list = response.css("p::text").extract()
        li_list = response.css("li::text").extract()
        font_list = response.css("font::text").extract()
        div_list = response.css("div::text").extract()
        strong_list = response.css("strong::text").extract()
        job['description'] = " ".join(span_list).strip('\r\n') + " ".join(p_list).strip('\r\n') + " ".join(li_list).strip('\r\n') + " ".join(font_list).strip('\r\n') + " ".join(div_list).strip('\r\n') + " ".join(strong_list).strip('\r\n')
        return job