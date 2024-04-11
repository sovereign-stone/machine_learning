import time
import ckpe
import jionlp as jio
from jionlp import keyphrase as jio_key
from temp.basic_conn import ConnectES

class UseJioNlp(object):
    def __init__(self):
        self.conn_es = ConnectES(hosts='10.125.0.43:9200', username='shijiuyi', password='MxuGFkxhW6Bbfayn')
        self.media = 'media_news'
        self.data_list = []
        self.remove_phrases_list = []
        self.remove_words_list = ['习近平']

    def use_ckpe(self, text, topic_theta=5, max_len=6):
        ckpe_obj = ckpe.ckpe()
        top_k = len(text) // 300
        top_k = min(max(top_k, 4), 9)
        key_phrases = ckpe_obj.extract_keyphrase(text, top_k=top_k, max_phrase_len=max_len, topic_theta=topic_theta,
                                                 remove_phrases_list=self.remove_phrases_list,
                                                 remove_words_list=self.remove_words_list)
        return key_phrases

    def extract_keyphrase(self, text, topic_theta=5, max_len=6, min_len=2):
        # top_k: 关键短语返回数量
        # max_phrase_len: 短语的最长长度
        # min_phrase_len: 短语的最短长度
        # topic_theta: 主题权重的权重调节因子，默认0.5，范围（0~无穷）
        # remove_phrases_list: 剔除不想要的短语
        # remove_words_list: 剔除不想要的词
        # specified_words: 行业名词:词频
        print(len(text))
        top_k = len(text) // 300
        top_k = min(max(top_k, 4), 9)
        key_phrases = jio_key.extract_keyphrase(text, top_k=top_k, max_phrase_len=max_len, min_phrase_len=min_len,
                                                topic_theta=topic_theta, remove_phrases_list=self.remove_phrases_list,
                                                remove_words_list=self.remove_words_list)
        return key_phrases

    @staticmethod
    def xiehouyu(keyword='王婆卖瓜'):
        res = []
        xhy_list = jio.xiehouyu_loader()
        result = [item for item in xhy_list if keyword in item[0]]
        for j in result:
            tar = j[0] + ' -- ' + j[1]
            res.append(tar)
        print(res)

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
            # s_tags = self.use_ckpe(text=content)
            print(ids, title)
            print(s_tags)
            print()

    def use_jionlp(self, url=None, title=None):
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
            # tags = self.extract_keyphrase(text=content)
            tags = self.use_ckpe(text=content)
            print(ids, title)
            print(tags)
        elif count > 1:
            print('搜索结果有多个，请提供更准确的搜索条件')
        else:
            print('搜索结果为空，请检查搜索条件')

    def run(self):
        # self.xiehouyu(keyword='一头')
        # self.extract_tags(size=100)
        # self.use_jionlp(url='https://news.ltn.com.tw/news/world/breakingnews/4587311')
        self.use_jionlp(title='韩朝野国会选举选区谈判陷入僵局')

        # one = '本文转载自 美国之音 ，仅代表原出处和原作者观点，仅供参考阅读，不代表本网态度和立场。 一项最新公布的研究表明，中国这个全球最大的碳排放大国由于最近批准新建十多家煤电厂，有可能无法兑现其在应对气候变化方面所作的减排承诺和目标。 资料照：中国山西省河津县一座火力发电站冒着浓烟的烟囱。 (2019年11月28日) 中国曾与美国及欧洲国家合作，承诺减排和推动绿能，以应对气候变化给全球带来的严重挑战。中国政府承诺要在2030年实现碳达峰，然后在2060年实现碳中和。为了实现这一雄心勃勃的目标，北京当局曾誓言“严控”新的煤电厂建设，并且破天荒地将大量风电和太阳能发电并入国家电网。 但是根据美国智库“全球能源检测”（GEM）和赫尔辛基“能源和清洁空气研究中心”（CREA）所作的最新研究，中国由于在新冠疫情肆虐的2021年曾发生多地严重缺电的状况，因此便在新建煤电厂申请和审批程序上大开绿灯。此举有可能迟滞中国从化石能源向清洁能源转变的步伐。 美国有线电视新闻网（CNN）引述研究报告的数据报道说，中国在短短两年中就已经批准新建产能高达218兆瓦的煤电厂，而218兆瓦煤电厂的发电量足够满足巴西的用电需求。 CNN根据分析报告报道说，中国政府去年批准新建114兆瓦的煤电厂，比一年前增10%。去年开始动工的新煤电厂产能约70兆瓦，也比一年前的54兆瓦有显著增加。去年投入运营的新建煤电厂产能约为47兆瓦，同样比一年前的28兆瓦有大幅增长。 研究报告指出，为了实现2025年减少碳排放和降低碳排放强度的目标，目前需要采取“紧迫的行动”，而且中国另一个在2025年实现将非化石能源在其总能源中的份额提升到20%的目标可以也难以如愿。 CNN引述研究人员的话说，中国整体的发电量其实已经足以满足需求，但是效率不高的中国电网系统却无法将电能输送到有需要的地区，尤其是这种需求需要跨省市的话。这就迫使中国要建立更多的电厂。 能源和清洁空气研究中心此前曾预测，随着更多清洁能源并网发电，北京对煤电厂的依赖将大幅减少，因此中国的碳排放量今年也会开始下降。 “这将给煤电厂的运营者带来巨大财务困难的风险，并且可能导致对能源转化的反弹，”CNN引述能源和清洁空气研究中心首席分析师劳里·迈利维尔塔（Lauri Myllyvirta）的话说。 “中国若要实现重返碳中和轨道所需的碳减排目标，这个矛盾就必须解决，”迈利维尔塔又说。 路透社引述迈利维尔塔星期四在“碳简报”网站（Carbon Brief）另外撰写的一篇文章说，中国2023年的碳排放量估计同比增长5.2%，而且自2020年以来已经增长12%。 迈利维尔塔指出，中国政府为了实现在2020年基础上将碳排放强度减少18%的目标，就必须在2025年之前将碳排放量减少4-6%。碳排放强度是指每单位国民生产总值的增长所带来的二氧化碳排放量。碳排放强度被用来衡量一国经济与碳排放量之间的关系。 本文转载自 美国之音 ，仅代表原出处和原作者观点，仅供参考阅读，不代表本网态度和立场。'
        # two = '以军再攻加萨纳瑟医院 世卫盼撤140名患者 （中央社）巴勒斯坦当局称以色列军队撤离加萨纳瑟医院（Nasser Hospital）后又再度进攻，世界卫生组织（WHO）官员昨（22）日表示，援助机构希望能疏散滞留在医院内的约140名患者。 《路透社》报导，加萨卫生部表示，医疗团队在医院院区内埋葬了13名因医院断电或缺乏氧气供应而丧命的患者。纳瑟医院位于汗尤尼斯（Khan Younis），是加萨地区第二大医院。 世卫表示，纳瑟医院对该地区脆弱的医疗服务至关重要，医院上週在以色列的围攻下暂停运作。 世卫加萨地区紧急事件团队负责人沙巴贝科夫（Ayadil Saparbekov）在记者会上表示，世卫和其他合作伙伴目前为止已在纳瑟医院进行3次疏散，最近一次是在21日，共有51名患者被转送到加萨南部。 沙巴贝科夫说：「世卫将继续尝试把纳瑟医院重症和重伤患者转送到南部其他医院，包括在拉法（Rafah）设置的战地医院，然而这是一项非常困难且高风险的任务。」 加萨卫生部表示，以色列部队原本已从纳瑟医院撤出，驻扎在附近，并禁止人员进出医院，随后又再次攻击这间医院。 沙巴贝科夫说，留在医院内的患者人数每个小时都在变化，有些人为了躲避战火而离开，有些人则伤重不治。 加萨卫生部21日稍早曾发布声明称有110名患者正在等待撤离，还说医院过去4天有8名患者因缺乏电力和氧气供给而丧命，他们的遗体已经开始腐败，对其他患者构成威胁。 加萨童身心受创 无国界医生：连5岁孩都说不想活 （中央社）以哈战争延烧，「无国界医生组织」昨天告诉联合国安全理事会，倖存的加萨孩童不仅身体受伤，目睹亲人遭肢解更让他们饱受心理创伤，甚至有5岁幼儿都说不想活了。 《路透社》报导，「无国界医生组织」（Doctors Without Borders）秘书长洛克伊尔（Christopher Lockyear）向联合国安理会表示，在加萨走廊（Gaza Strip）的医疗团队发明了一个新的缩写词汇WCNSF，意即「没有亲人倖存的受伤孩童」（wounded child, no surviving family）。 他说：「在这场战争倖存的孩童不仅遭受眼睛可见的创伤，也承受肉眼看不见的痛苦。」 「他们不断被迫迁移，时时处于恐惧，甚至还看到亲人在自己眼前遭肢解…这些心理创伤让年仅5岁的幼儿都告诉我们，他们宁愿死掉。」 洛克伊尔也抨击美国一而再地动用否决权，阻止安理会通过要求以色列及巴勒斯坦武装组织「哈玛斯」（Hamas）立即在加萨人道停火的决议，这让他备感震惊。 他说，加萨人民需要停火协议，「不是在可行的时候，而是现在。他们需要的是持续停火，而非暂时的冷静期」。 自以哈双方去（2023）年10月7日爆发战争以来，美国已3度否决联合国安理会有关以哈战争的决议草案，最近一次是2月20日否决了立即人道停火的要求，但敦促安理会要求以哈暂时停火，以让哈玛斯释放在去年10月7日突袭以色列时掳走的人质。 中国驻联合国大使张军告诉安理会，他对洛克伊尔的简报内容感到震惊，「我们希望他所描述的加萨悲惨情况能触动安理会某个理事国的良心」。 美国先前表示，美方20日动用否决权是因为担忧这项决议草案恐损及美国、埃及、以色列及卡达设法促成休战6週及释放人质的会谈。 美国驻联合国副大使伍德（Robert Wood）并未对洛克伊尔的简报表示认同。他说，美国一直在促使以色列让更多援助进入加萨，也已告诉这个盟友，不应「在没有可行的保护平民计画下」，对加萨南部城市拉法（Rafah）发动攻势。 伍德说，「我们都希望看到冲突划下永久句点」，「有关人质的谈判步调可能会令人受挫…安理会支持这项外交行动对加强施压哈玛斯接受协议来说至关重要」。 新闻来源 以军再攻加萨纳瑟医院 世卫盼撤140名患者（中央社） 加萨童身心受创 无国界医生：连5岁孩都说不想活（中央社） 延伸阅读 美3度否决安理会以哈战争决议草案；以色列准备进攻拉法，拜登更频繁使用「停火」一词，联合国：加萨饥荒迫在眉睫 加萨人道危机：第2大医院仅剩4名医护苦撑，美国扬言否决安理会停火案，联合国援巴机构也断炊 联合国机构高度垄断加萨「难民产业」，在当地出高薪养出一代又一代仇美反犹的巴勒斯坦人 【加入关键评论网会员】每天精彩好文直送你的信箱，每週独享编辑精选、时事精选、艺文週报等特制电子报。还可留言与作者、记者、编辑讨论文章内容。 立刻点击免费加入会员！ 责任编辑：杨佳臻 核稿编辑：杨士范'
        # three = '有记者提问：美国众议院中国问题特别委员会主席加拉格尔致信大众汽车，要求该公司立即遵守所谓“维吾尔强迫劳动预防法”，并且停止其在新疆的运营。外交部对此有何评论？ 毛宁对此表示，中方已经多次指出，所谓 新疆 存在“强迫劳动”，完全是反华势力为抹黑中国炮制出的谎言。美国以根本不存在的所谓新疆“强迫劳动”为借口，将正常的经贸合作政治化，违反国际贸易规则，扰乱市场正常秩序，最终也将损害美国自身的利益。'
        # tags = self.extract_keyphrase(text=three)
        # print(tags)
        pass


if __name__ == '__main__':
    start = time.time()
    fix_cn = UseJioNlp()
    fix_cn.run()
    end = time.time()
    print(f'spend time : {round(end - start, 2)}')
