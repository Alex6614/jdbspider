# -*- coding: utf-8 -*-
import scrapy, logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jdbspider.items import jobItem
from lxml import etree


class SimplespiderSpider(CrawlSpider):
    name = 'simplespider'
    allowed_domains = ['hk.jobsdb.com']
    start_urls = ['https://hk.jobsdb.com/hk/search-jobs/big-data/1']
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
        job['description'] = " ".join(span_list)
        return job