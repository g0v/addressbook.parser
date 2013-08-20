# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from json import dumps
import codecs

class JsonWriterPipeline(object):

    def __init__(self):
        self.file_name = "../raw_data/oid.json"

    def process_item(self, item, spider):
        """
        Save data to json format, this will use file_name to save
        """
        with codecs.open(self.file_name, 'w', 'utf-8') as f:
            f.write(dumps(item, ensure_ascii = False, indent=4))

        return item
