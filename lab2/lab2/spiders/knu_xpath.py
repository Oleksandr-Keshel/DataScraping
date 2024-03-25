import scrapy
from ..items import FacultyItem, DepartmentItem


class KnuXpathSpider(scrapy.Spider):
    name = "knu_xpath"
    allowed_domains = ["knu.ua"]
    start_urls = ["https://knu.ua/ua/departments"]

    def parse(self, response):
        faculties_list = response.xpath('//ul[@class="b-references__holder"]')[0].xpath('.//li[@class="b-references__item"]')
        for faculty in faculties_list:
            faculty_name = faculty.xpath('.//a/text()').get()
            faculty_url = f"https://knu.ua/{faculty.xpath('.//a/@href').get()}"
            yield FacultyItem(
                name=faculty_name,
                url=faculty_url
            )
            yield scrapy.Request(
                # адреса сторінки, яку необхідно парсити
                url=faculty_url,
                # метод для обробки результатів завантаження
                callback=self.parse_faculty,
                # передаємо дані про факультет в функцію колбеку
                meta={
                    "faculty": faculty_name
                }
            )

    def parse_faculty(self, response):
        depart_list = response.xpath('.//ol/li[@class="b-body__text"]')
        for li in depart_list:
            if li.xpath('.//a'):
                depart_name = li.xpath('.//a/text()').get()
                depart_url = li.xpath('.//a/@href').get()
            else:
                depart_name = li.xpath('.//text()').get()
                depart_url = "No URL"
            yield DepartmentItem(
                name=depart_name,
                url=depart_url,
                faculty=response.meta.get("faculty")
            )
