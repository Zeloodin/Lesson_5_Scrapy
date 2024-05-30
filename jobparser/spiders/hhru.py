import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://chelyabinsk.hh.ru/search/vacancy?text=python&area=104&hhtmFrom=main&hhtmFromLabel=vacancy_search_line"]

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("""//a[@data-qa="pager-next"]/@href""").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


        links = response.xpath("""//span[@class="serp-item__title-link-wrapper"]//@href""").getall()
        # print(response.status, response.url)
        # print(len(links), links)
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)



    def vacancy_parse(self, response:HtmlResponse):
        # # name = response.xpath("""//h1[@data-qa="vacancy-title"]""").get()
        # # name = response.xpath("//h1/text()").getall()
        # #
        # name = response.xpath("//h1/text()").getall()
        # salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()

        #
        # name = response.xpath("//h1[@data-qa='vacancy-title']//span").getall()
        # name = response.xpath("//h1/text()").get()

        # name = response.xpath("//div[@class='vacancy-title']/h1[@data-qa]//ext()").get()
        # salary = response.xpath("//div[@data-qa='vacancy-salary']//span/text()").getall()

        salary = response.xpath("//div[@data-qa='vacancy-salary']//span/text()").getall()
        name = response.xpath("//h1/text()").get()
        if not salary:
            salary = "Уровень дохода не указан"
        url = response.url
        # print(name, salary, url)
        #
        # print(name,salary)
        yield JobparserItem(name=name,salary=salary,url=url)
