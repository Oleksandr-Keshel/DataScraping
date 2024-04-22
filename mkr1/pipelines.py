# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import SmartphoneItem, ShopItem


class Mkr1Pipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name == 'image_urls':
                adapter[field_name] = value[0].strip()
            else:
                adapter[field_name] = value.strip()

            if isinstance(item, ShopItem) and field_name == 'price':
                adapter[field_name] = float(item.get(field_name).replace("\xa0", ""))
        return item
