import scrapy
import json

from marco.items import Person
from marco import constants


class LocateSpider(scrapy.Spider):
    """
    obtener ubigeo por provincias
    perdon por el espaguetti, lo hice en una noche
    """
    name = 'locate'
    global_ubigeo = {}

    father_lastname = ''
    mother_lastname = ''
    person_name = ''
    print 'Buscando...'

    def start_requests(self):
        self.father_lastname = raw_input('Apellido paterno: ')
        self.mother_lastname = raw_input('Apellido materno: ')
        self.person_name = raw_input('Nombre: ')

        url = ''.join([
            'http://consultamiembrodemesa.onpe.gob.pe/',
            'consultamm_eg_2016/default/index/consultaUbigeoPro'])
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        request_list = []

        for ubigeo in constants.FIRST_REGIONS.keys():
            meta = {'dep_ubigeo': ubigeo,
                    'dep_name': constants.FIRST_REGIONS[ubigeo]}
            request_list.append(scrapy.FormRequest(
                url,
                headers=headers,
                formdata={'ubigeo': ubigeo},
                meta=meta,
                callback=self.process_pro))
        return request_list

    def process_pro(self, response):
        url = ''.join([
            'http://consultamiembrodemesa.onpe.gob.pe/',
            'consultamm_eg_2016/default/index/consultaUbigeoDis'])
        headers = {'X-Requested-With': 'XMLHttpRequest'}

        ubigeo_dict = {
                ele.xpath('@value').extract()[0]:
                ele.xpath('text()').extract()[0]
                for ele in response.xpath('//option')}

        for ubigeo in ubigeo_dict.keys():
            meta = response.meta
            meta['pro_ubigeo'] = ubigeo
            meta['pro_name'] = ubigeo_dict[ubigeo]

            yield scrapy.FormRequest(
                url,
                headers=headers,
                formdata={'ubigeo': ubigeo},
                meta=meta,
                callback=self.process_dis)

    def process_dis(self, response):
        ubigeo_dict = {
                ele.xpath('@value').extract()[0]:
                ele.xpath('text()').extract()[0]
                for ele in response.xpath('//option')}

        for ubigeo in ubigeo_dict.keys():
            meta = response.meta
            meta['dis_ubigeo'] = ubigeo
            meta['dis_name'] = ubigeo_dict[ubigeo]

            url_pattern = ''.join([
                '{domain}{path}?appaterno={appaterno}',
                '&apmaterno={apmaterno}&nombres={nombres}',
                '&dep={dep}&pro={pro}&dis={dis}'])

            url = url_pattern.format(
                    domain='http://consultamiembrodemesa.onpe.gob.pe/',
                    path='consultamm_eg_2016/default/index/listado',
                    appaterno=self.father_lastname,
                    apmaterno=self.mother_lastname,
                    nombres=self.person_name,
                    dep=response.meta['dep_ubigeo'],
                    pro=response.meta['pro_ubigeo'],
                    dis=ubigeo)
            yield scrapy.Request(url, callback=self.proces_listado, meta=meta)

    def proces_listado(self, response):
        body = json.loads(response.body)
        if body['data'][0]:
            person = Person()
            person['dep_ubigeo'] = response.meta['dep_ubigeo']
            person['dep_name'] = response.meta['dep_name']
            person['pro_ubigeo'] = response.meta['pro_ubigeo']
            person['pro_name'] = response.meta['pro_name']
            person['dis_ubigeo'] = response.meta['dis_ubigeo']
            person['dis_name'] = response.meta['dis_name']
            person['nombres'] = body['data'][0]['nombres']
            person['ap_paterno'] = body['data'][0]['apPaterno']
            person['ap_materno'] = body['data'][0]['apMaterno']
            person['dni'] = body['data'][0]['dni']
            print body['data'][0]
            yield person
