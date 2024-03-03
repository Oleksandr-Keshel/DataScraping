# https://knu.ua/ua/departments
from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://knu.ua"
URL = f"{BASE_URL}/ua/departments"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
page = get(URL, headers=HEADERS)
# print(page.text)

soup = BeautifulSoup(page.content,  "html.parser")

faculties_list = soup.find(class_="b-references__holder")
FILE_NAME = "knu.txt"
with open(FILE_NAME, "w", encoding="utf-8") as file:
    for li in faculties_list.find_all("li"):
        a = li.find("a")
        faculty_name = a.find(string=True, recursive=False)  # a.string
        faculty_url = BASE_URL + a.get('href')  # a.attrs["href"]
        print(f"Faculty name: {faculty_name}")
        print(f"URL: {faculty_url}")
        file.write(f"Faculty name: {faculty_name}")
        file.write(f" URL: {faculty_url}\n")

        faculty_page = get(faculty_url, headers=HEADERS)
        soup = BeautifulSoup(faculty_page.content,  "html.parser")
        depart_list = soup.find("ol")
        for li in depart_list.find_all("li"):
            if li.find("a"):
                a = li.find("a")
                depart_name = a.find(string=True, recursive=False)  # a.string
                depart_url = BASE_URL + a.get('href')  # a.attrs["href"]
            else:
                depart_name = li.find(string=True, recursive=False)
                depart_url = "No URL"
            print(f"\tDepartment name: {depart_name}")
            print(f"\tURL: {depart_url}")
            file.write(f"\tDepartment name: {depart_name}")
            file.write(f"\tURL: {depart_url}\n")




