# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import docscraper.models.database as database


class DocscraperPipeline:
    def process_item(self, item, spider):
        return item


class SqlitePipeline:
    def __init__(self):
        database.setup_database()

    def open_spider(self, spider):
        database.db.connect("docscraper.db")
        database.db.create_tables([database.Doctors, database.Licenses, database.Doctors_Licenses])

    def close_spider(self, spider):
        database.db.close()

    def process_item(self, item, spider):
        # todo: add additonal fields to database, when scraping is actually implemented
        # todo: deduplication
        database.Doctors.insert(dict(item)).execute()
        # todo: actually scrape license types and pray this works
        for license_type in item["license_type"]:
            database.Licenses(
                license_type=license_type, doctor_id=item["doctor_id"],
            ).save()
        return item
