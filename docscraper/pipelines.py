# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import docscraper.database as database


class DocscraperPipeline:
    def process_item(self, item, spider):
        return item


class SqlitePipeline:
    def __init__(self):
        database.setup_database()

    def open_spider(self, spider):
        database.db.connect("docscraper.db")
        database.db.create_tables([database.Doctors, database.Licenses])

    def close_spider(self, spider):
        database.db.close()

    def process_item(self, item, spider):
        # todo: add additonal fields to database, when scraping is actually implemented
        # todo: deduplication
        database.Doctors(
            name=item["name"],
            profile_url=item["profile_url"],
            doctor_id=item["doctor_id"],
            field_of_work=item["field_of_work"],
            address=item["address"],
            phone=item["phone"],
            email=item["email"],
            fax=item["fax"],
            website=item["website"],
            office_type=item["office_type"],
        ).save()
        # todo: actually scrape license types and pray this works
        for license_type in item["license_type"]:
            database.Licenses(
                license_type=license_type, doctor_id=item["doctor_id"],
            ).save()
        return item


# unfinished and most likely not compatible with sqlite ??
class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["id"] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter["id"])
            return item
