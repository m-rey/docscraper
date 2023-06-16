# docscraper

1. Install python-dotenv, peewee and scrapy with pip or conda

2. create an .env file in the root of this repository from the following example:
```
# For other configs, search on https://dienste.kvb.de/arztsuche/app/erweiterteSuche.htm
# and look for outgoing POST requests.
# Try to use 'landkreise' to filter results. Don't use 'adresse' for filtering, as it doesn't filter results.
# Instead, 'adresse' affects the sort order and shows nearby results first.
# You can specify multiple entries, as long as they are separated by semicolons.

LANDKREISE=09564000
GENEHMIGUNGEN=Verhaltenstherapie Erwachsene; Verhaltenstherapie Erwachsene, Gruppe
```

3. run ```scrapy crawl kvb```

4. You should now have a sqlite database called docscraper.db