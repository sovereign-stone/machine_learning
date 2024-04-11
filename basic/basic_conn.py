import redis
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from basic.basic_addr import *


class ConnectRedis(object):
    def __init__(self, host=redis_host, db=0, port=redis_port, password=redis_pwd):
        self.red = redis.StrictRedis(host=host, port=port, db=db, password=password,
                                     decode_responses=True, charset='UTF-8', encoding='UTF-8')


class ConnectES(object):
    def __init__(self, mode='dev'):
        if mode == 'dev':
            hosts = es_hosts_dev
            username = es_name_dev
            password = es_pwd_dev
        else:
            hosts = es_hosts
            username = es_name
            password = es_pwd
        if username and password:
            self.conn_es = Elasticsearch([hosts], http_auth=(username, password), request_timeout=120)
        else:
            self.conn_es = Elasticsearch([hosts], request_timeout=120)

    def es_body_search(self, index, body):
        result = self.conn_es.search(index=index, body=body, request_timeout=60)
        return result

    def update_es_one_data(self, index, ids, update_dict):
        # update es one data: {"doc": {"distinct": ""}}
        if ids:
            self.conn_es.update(index=index, id=ids, body=update_dict)
        else:
            self.conn_es.index(index=index, body=update_dict)

    def index_es_one_data(self, index, ids, data):
        if ids:
            self.conn_es.index(index=index, id=ids, body=data, doc_type='_doc')
        else:
            self.conn_es.index(index=index, body=data, doc_type='_doc')

    def bulk_insert_data(self, list_data):
        """
        helpers.bulk insert data to es, 字典里面包括_index, _type, _id, _source
        example:
            one_dict = {}
            one_dict['_index'] = index
            one_dict['_id'] = j['domain']
            one_dict['_type'] = "_doc"
            one_dict['_source'] = j
            es_list.append(one_dict)

        :param list_data: type is list
        :return: insert paste time
        """
        start_time = datetime.datetime.now()
        helpers.bulk(self.conn_es, list_data)
        end_time = datetime.datetime.now()
        paste_time = end_time - start_time
        return paste_time
