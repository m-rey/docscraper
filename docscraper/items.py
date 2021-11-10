# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KvbItem(scrapy.Item):
    name = scrapy.Field()
    profile_url = scrapy.Field()
    doctor_id = scrapy.Field()
    field_of_work = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    fax = scrapy.Field()
    website = scrapy.Field()
    office_type = scrapy.Field()
    distance = scrapy.Field()
