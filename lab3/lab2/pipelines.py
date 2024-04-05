# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import FacultyItem, DepartmentItem
import mysql.connector


class Lab2Pipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if isinstance(item, FacultyItem) and field_name == 'image_urls':
                adapter[field_name] = value[0].strip()
            else:
                adapter[field_name] = value.strip()
        return item



class MySqlPipeline:
    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password="",
            database="scrapyDB",
        )
        self.cursor = self.connection.cursor()
        spider.logger.info("Connected to MySQL")
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS 
                faculty_items (
                    id INT AUTO_INCREMENT,
                    PRIMARY KEY (id),
                    name VARCHAR(60) NOT NULL,
                    url VARCHAR(500),
                    image_urls VARCHAR(500)
                )""")
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS 
                department_items (
                    id INT AUTO_INCREMENT,
                    PRIMARY KEY (id),
                    name VARCHAR(120) NOT NULL,
                    url VARCHAR(500),
                    faculty VARCHAR(60) NOT NULL
                )""")
        spider.logger.info("DB is ready ")

    def close_spider(self, spider):
        self.connection.close()
        spider.logger.info("Disconnected from MySQL")

    def process_item(self, item, spider):
        # processing FacultyItem
        if isinstance(item, FacultyItem):
            if self.is_duplicate(item):
                self.cursor.execute("""
                                        UPDATE faculty_items
                                        SET url = %s
                                        WHERE name = %s
                                        """,
                                    [item.get("url"), item.get("name")]
                                    )
            else:
                self.cursor.execute(
                                    "INSERT INTO faculty_items (name, url, image_urls) VALUES (%s, %s, %s);",
                                    [item.get("name"), item.get("url"), item.get("image_urls")]
                                    )

        # processing DepartmentItem
        if isinstance(item, DepartmentItem):
            if self.is_duplicate(item):
                self.cursor.execute("""
                                        UPDATE department_items
                                        SET url = %s
                                        WHERE name = %s
                                        """,
                                    [item.get("url"), item.get("name")]
                                    )
            else:
                self.cursor.execute(
                                    "INSERT INTO department_items (name, url, faculty) VALUES (%s, %s, %s);",
                                    [item.get("name"), item.get("url"), item.get("faculty")]
                                    )

        self.connection.commit()
        return item

    def is_duplicate(self, item):
        if isinstance(item, FacultyItem):
            self.cursor.execute(
                "SELECT COUNT(id) FROM faculty_items WHERE name = %s;",
                [item.get("name")])
            count = self.cursor.fetchone()[0]
        if isinstance(item, DepartmentItem):
            self.cursor.execute(
                "SELECT COUNT(id) FROM department_items WHERE name = %s;",
                [item.get("name")])
            count = self.cursor.fetchone()[0]
        return count > 0
