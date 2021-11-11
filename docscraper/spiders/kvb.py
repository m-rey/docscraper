import scrapy
import os

from docscraper.items import KvbItem
from scrapy.exceptions import CloseSpider
from dotenv import load_dotenv


load_dotenv()
LANDKREISE = os.getenv("LANDKREISE").split(";")
GENEHMIGUNGEN = os.getenv("GENEHMIGUNGEN").split(";")


class KvbSpider(scrapy.Spider):
    name = "kvb"
    allowed_domains = ["kvb.de"]

    def start_requests(self):

        search_query = {
            "genehmigungen": GENEHMIGUNGEN,
            "landkreise": LANDKREISE,
        }

        return [
            scrapy.FormRequest(
                url="https://dienste.kvb.de/arztsuche/app/erweiterteSucheAusfuehrung.htm",
                formdata=search_query,
                callback=self.add_params,
            )
        ]

    def add_params(self, response):
        # override the default total result limit of 100 and prevent loading useless google maps in search results
        url = response.url + "&zeigeKarte=false&resultCount=10000"
        return scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        results = response.css(".suchergebnisse_praxis_innere_tabelle")
        for result in results:

            item = KvbItem()

            # TODO: replace this with ItemLoader
            item["name"] = (
                result.css(".titel_name_zelle > a::text").get(default="").strip()
            )
            item["profile_url"] = (
                "https://dienste.kvb.de"
                + result.css(".titel_name_zelle > a::attr(href)")
                .get(default="")
                .strip()
            )
            # profile_url ends with 'arztCode=<id>'
            item["doctor_id"] = item["profile_url"].split("=")[-1]
            item["field_of_work"] = (
                result.css(".fachgebiet_zelle::text").get(default="").strip()
            )
            item["address"] = "\n".join(
                result.css(".adresse_tabelle tr td::text").re(r"(\S.*\S)|\S")
            )
            item["phone"] = (
                result.css(".tel_td:contains('Tel.:') + td::text")
                .get(default="")
                .strip()
            )
            item["email"] = (
                result.css(".tel_tabelle tr > td:contains('E-Mail:') + td > a::text")
                .get(default="")
                .strip()
            )
            item["office_type"] = (
                result.css(".adresse_zelle.leere_zeile > span::text")
                .get(default="")
                .strip()
            )
            item["fax"] = (
                result.css(".tel_td:contains('Fax.:') + td::text")
                .get(default="")
                .strip()
            )
            item["website"] = (
                result.css(".tel_td:contains('Web:') + td > a::text")
                .get(default="")
                .strip()
            )

            yield item

        xpath_next_page = (
            '//form[@action="suchergebnisse.htm"]/input[@class="BUTTON FORWARD"]/..'
        )
        # go to next page and parse it, if there is one
        if response.xpath(xpath_next_page):
            yield scrapy.FormRequest.from_response(
                response,
                formxpath=xpath_next_page,
                callback=self.parse,
            )
        else:
            raise CloseSpider("No more search results")
