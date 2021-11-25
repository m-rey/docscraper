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
        pass

    def close_spider(self, spider):
        database.session.commit()

    def process_item(self, item, spider):
        # todo: deduplication
        doctor = database.Doctor(
            name=item["name"],
            profile_url=item["profile_url"],
            doc_nr=item["doc_nr"],
            field_of_work=item["field_of_work"],
            address=item["address"],
            phone=item["phone"],
            email=item["email"],
            office_type=item["office_type"],
            fax=item["fax"],
            website=item["website"],
            lanr=item["lanr"],
            bsnr=item["bsnr"],
        )
        database.session.add(doctor)
        database.session.flush()  # unsure if this is better done here or in close_spider()

        return item
