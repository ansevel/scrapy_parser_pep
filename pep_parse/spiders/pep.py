import re

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        for pep in response.css('section#numerical-index tbody tr'):
            pep_link = pep.css('a::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        pattern = r'^PEP (?P<number>\d+) – (?P<name>.+)'
        title_text = response.css('h1.page-title::text').get()
        text_match = re.search(pattern, title_text)
        number, name = text_match.group('number', 'name')
        data = {
            'number': number,
            'name': name,
            'status': response.css(
                'dt:contains("Status") + dd abbr::text').get()
        }
        yield PepParseItem(data)
