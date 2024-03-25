import scrapy
from ..items import FacultyItem, DepartmentItem


class KnuCssSpider(scrapy.Spider):
    name = "knu_css"
    allowed_domains = ["knu.ua"]
    start_urls = ["https://knu.ua/ua/departments"]

    def parse(self, response):
        faculties_list = response.css('ul.b-references__holder')[0].css('li.b-references__item')
        for faculty in faculties_list:
            faculty_name = faculty.css('a::text').get()
            faculty_url = f"https://knu.ua/{faculty.css('a::attr(href)').get()}"
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
        depart_list = response.css('ol li.b-body__text')
        for li in depart_list:
            if li.css('a'):
                depart_name = li.css('a::text').get()
                depart_url = li.css('a::attr(href)').get()
            else:
                depart_name = li.css('::text').get()
                depart_url = "No URL"
            yield DepartmentItem(
                name=depart_name,
                url=depart_url,
                faculty=response.meta.get("faculty")
            )
