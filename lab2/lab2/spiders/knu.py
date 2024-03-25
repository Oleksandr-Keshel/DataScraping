import scrapy
from bs4 import BeautifulSoup
from ..items import FacultyItem, DepartmentItem


class KnuSpider(scrapy.Spider):
    name = "knu"
    allowed_domains = ["knu.ua"]
    start_urls = ["https://knu.ua/ua/departments"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        faculties_list = soup.find(class_="b-references__holder")
        for li in faculties_list.find_all("li"):
            a = li.find("a")
            faculty_name = a.find(string=True, recursive=False)
            faculty_url = f"https://knu.ua{a.get('href')}"
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
        soup = BeautifulSoup(response.body, "html.parser")
        depart_list = soup.find("ol")
        for li in depart_list.find_all("li"):
            if li.find("a"):
                a = li.find("a")
                depart_name = a.find(string=True, recursive=False)
                depart_url = f"https://knu.ua{a.get('href')}"
            else:
                depart_name = li.find(string=True, recursive=False)
                depart_url = "No URL"
            yield DepartmentItem(
                name=depart_name,
                url=depart_url,
                faculty=response.meta.get("faculty")
            )
