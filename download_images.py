# /// script
# requires-python = ">=3.10"
# dependencies = ["scrapy", "pillow", "dataclasses"]
# ///

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from dataclasses import dataclass, field, asdict
from typing import Optional
from scrapy.pipelines.images import ImagesPipeline
import hashlib 
import random

class ImageItem(scrapy.Item):
    event_id = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


event_id_dicts = {

    "6809f906f1109cd9bae62d51": "THONON CYCLING RACE 2025",
    "667536785978751d5dd293bd": "MARMOTTE GRANFONDO ALPES 2024",
    "6629127f0561270b6ba24326": "LA VACHE QUI RIT 2024",
    "662911c80561270b6ba23fbf": "THONON CYCLING RACE 2024",
    "6491718f47a2b0bb3f2dbd69": "MARMOTTE GRANFONDO ALPES 2023",
    "64356e67096174539781585a": "LA VACHE QUI RIT 2023",
    "64356ed009617453978159fe": "THONON CYCLING RACE 2023",
    "624f080ee140a3651b340d15": "MARMOTTE GRANFONDO ALPES 2022",
}

scrapy_settings = {
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    "ITEM_PIPELINES": {
        "__main__.PhotoBretonImagePipeline": 1,
    },
    "IMAGES_STORE": "images/",
}

def main() -> None:
    print("Hello from download_images.py!")



class PhotoBretonSpider(scrapy.Spider):
    name = "phtots_url"
    base_url = "https://www.photobreton.com"

    def get_page_url(self, event_id: str, bib_number: str):
        return f"{self.base_url}/?selected_Folder_id={event_id}&T=F&Tpl=1&nbrOfFields=2&advancedSearch=valider&regex_A2-1=2&Name_A2-1={bib_number}&npp=100"

    def __init__(self, event_id:str, bib_range: list[int], *args, **kwargs):
        super(PhotoBretonSpider, self).__init__(*args, **kwargs)
        self.event_id = event_id
        self.bib_range = bib_range
        self.start_urls = [
        self.get_page_url(event_id, str(i)) for i in bib_range
    ]

    def parse(self, response):
        for item in response.css("span.ThmbBlckImg"):
            image = ImageItem()
            url = self.base_url + item.css("img").attrib["src"]
            url = url.replace("SMALL", "MEDIUM")
            image["event_id"] = self.event_id
            image["image_urls"] = [url]
            yield image


class PhotoBretonImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
        return f"{item.get('event_id', 'unknown_event')}/{url_hash}.jpg"
    
def get_random_bib_range(MAX_BIB = 10000, num=20) -> list[int]:
    dossards =random.sample(range(1, MAX_BIB + 1), num)
    return sorted(dossards)

if __name__ == "__main__":
   
    settings = Settings()
    for key, value in scrapy_settings.items():
        settings.set(key, value)

    process = CrawlerProcess(settings)
    
    for event in event_id_dicts.keys():
        bib_range =  get_random_bib_range()
        process.crawl(PhotoBretonSpider, event_id=event, bib_range=bib_range)
    
    process.start()     