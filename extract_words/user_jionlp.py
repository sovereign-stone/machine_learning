import time
import jionlp as jio
from loguru import logger
from jionlp import keyphrase as jio_key
from basic.basic_conn import ConnectES

class UseJioNlp(object):
    def __init__(self):
        self.conn_es = ConnectES(mode='pro')
        self.media = 'media_news'
        self.data_list = []
        self.remove_phrases_list = []
        self.remove_words_list = ['习近平']

    @staticmethod
    def xiehouyu(keyword='王婆卖瓜'):
        res = []
        xhy_list = jio.xiehouyu_loader()
        result = [item for item in xhy_list if keyword in item[0]]
        for j in result:
            tar = j[0] + ' -- ' + j[1]
            res.append(tar)
        print(res)

    def extract_keyphrase(self, text, topic_theta=5, max_len=6, min_len=2):
        # top_k: 关键短语返回数量
        # max_phrase_len: 短语的最长长度
        # min_phrase_len: 短语的最短长度
        # topic_theta: 主题权重的权重调节因子，默认0.5，范围（0~无穷）
        # remove_phrases_list: 剔除不想要的短语
        # remove_words_list: 剔除不想要的词
        # specified_words: 行业名词:词频
        logger.info(f'文本长度为: {len(text)}')
        top_k = len(text) // 200
        top_k = min(max(top_k, 4), 9)
        key_phrases = jio_key.extract_keyphrase(text, top_k=top_k, max_phrase_len=max_len, min_phrase_len=min_len,
                                                topic_theta=topic_theta, remove_phrases_list=self.remove_phrases_list,
                                                remove_words_list=self.remove_words_list)
        return key_phrases

    def extract_tags(self, size=1000):
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "publish_time": {
                                    "gte": "2024-01-01 00:00:00",
                                    "lt": "2024-03-01 00:00:00"
                                }
                            }
                        },
                        {
                            "script": {
                                "script": "doc['system_tags'].size() == 0"
                            }
                        }
                    ]
                }
            },
            "sort": [
                {
                    "@timestamp": {
                        "order": "desc"
                    }
                }
            ],
            "size": size,
            "track_total_hits": True
        }
        res = self.conn_es.es_body_search(index=self.media, body=body)
        datas = res['hits']['hits']
        for j in datas:
            source = j['_source']
            ids = j['_id']
            title = source['title']
            content = source['content']
            s_tags = self.extract_keyphrase(text=content)
            print(ids, title)
            print(s_tags)
            print()

    def jionlp_parse(self, url=None, title=None):
        query = []
        if url:
            query.append({"term": {"url": {"value": url}}})
        elif title:
            query.append({"regexp": {"title": f".*{title}.*"}})
        else:
            print('没有对该字段的搜索')
            return False
        body = {"query": {"bool": {"must": query}}}
        res = self.conn_es.es_body_search(index='media', body=body)
        count = res['hits']['total']['value']
        if count == 1:
            data = res['hits']['hits'][0]['_source']
            ids = data['uuid']
            title = data['title']
            content = data.get('content', '')
            tags = self.extract_keyphrase(text=content)
            print(ids, title)
            print(tags)
        elif count > 1:
            print('搜索结果有多个，请提供更准确的搜索条件')
        else:
            print('搜索结果为空，请检查搜索条件')

    def run(self):
        # self.xiehouyu(keyword='一头')
        # self.extract_tags(size=100)
        # self.jionlp_parse(url='https://news.ltn.com.tw/news/world/breakingnews/4587311')
        self.jionlp_parse(title='韩朝野国会选举选区谈判陷入僵局')
        pass


if __name__ == '__main__':
    start = time.time()
    fix_cn = UseJioNlp()
    fix_cn.run()
    end = time.time()
    print(f'spend time : {round(end - start, 2)}')
