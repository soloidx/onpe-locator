# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Person(scrapy.Item):
    dep_ubigeo = scrapy.Field()
    dep_name = scrapy.Field()
    pro_ubigeo = scrapy.Field()
    pro_name = scrapy.Field()
    dis_ubigeo = scrapy.Field()
    dis_name = scrapy.Field()
    nombres = scrapy.Field()
    ap_paterno = scrapy.Field()
    ap_materno = scrapy.Field()
    dni = scrapy.Field()
