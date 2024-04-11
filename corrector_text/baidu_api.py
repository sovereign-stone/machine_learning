import requests
import json
import redis


class HandlerMisSensitive(object):
    def __init__(self):
        self.ydy_red = redis.StrictRedis(host='10.125.0.28', port=6379, db=1, password='soc-ti-redis',
                                         decode_responses=True, charset='UTF-8', encoding='UTF-8')
        self.baidu_token = '24.fafa23f8f2bf8379d6c9da116d75664a.2592000.1715320328.282335-30118490'

    def baidu_correct(self, text):
        url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/text_correction?charset=&access_token=" + self.baidu_token

        payload = json.dumps({"text": text})
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        result = response.json()
        print(result)

    def run(self):
        con = '习近屏：继续保持密切交往，确保中俄关系始终顺利稳定向前发展'
        con2 = '河北省赵县的洨河上，有一座世界文明的石拱桥，叫安济桥，又叫赵州桥。它是隋朝的石匠李春涉及和参加建造的，到现在已经有一千三百多年了。赵州桥非常很雄伟，桥长五十多米，有九米多宽，中间行车马，两旁走人。这么长的桥，全部用石头砌成，下面没有桥礅，只有一个拱形的大桥洞，横跨在三十七米多宽的河面上。大桥洞顶上的左右两边，还各有两个拱形的小桥洞。平时，河水从大桥洞流过，发大水的时候，河水还可以从四个小桥洞溜过。这种设计，在建桥史上是创举一个，既减轻了流水对桥身的冲击力，使桥不容易被大水冲毁，又减轻了桥身的重量，节约石材.这座桥梁不仅结实而且漂亮。桥面两侧有石栏，栏板上雕刻着糊里糊涂的图案：有的刻着两条相互缠绕的龙，嘴里吐出美丽的水花；有的刻着两条飞龙，前爪相互抵着着，各自回首遥望；还有的刻着双龙戏珠。所有的龙似乎都在游动，真像活了一样。赵州桥表现了劳动人民的聪明才智，是我国宝贵的历史遗产。'
        con3 = '暴雪国服本周官宣回回归的话题冲上热搜，引起了巨大关注，尤其是老玩家非常激动。据国内媒体报道道，暴雪娱乐和网易公司确实在2023年底就开始接触，春节过后位于广州的网易互娱运营中心已经组建了暴雪国服的得封闭基地，主要负责日常运营、客服等等工作。'
        con4 = '在国内，年轻人职场的传说由来已久，在澳洲则恰恰，职场年轻人频频吐槽。 老板吐槽他们太懒、不愿意干活、动不动就请假。 HR吐槽他们眼高手低实际，对工资要求过高，刚来没多久就想加薪，一言不合就辞职。'
        con5 = '少先队员因该为老人让坐，你找到你最喜欢的工作，我也很高心。'
        con6 = '报应接中迩来，这块名表带带相传'
        con7 = '在这个五彩斑斓的世界里，年轻人们如同蝴蝶般自由地飞舞着，追逐着光芒和梦想。他们是生命中最美丽的花朵，却又像是一群迷失在迷宫中的小鸟，寻找着归宿。他们的心灵，像是一池湖水，波澜起伏，隐藏着无尽的秘密和欲望。他们的眼神，仿佛是闪烁的星星，充满了对未来的渴望和对世界的好奇。在这个快节奏的时代，他们被时光的车轮推向前行，无法停歇，无法回头。他们是青春的使者，是激情的火焰，是希望的载体。让我们一起为这群青年呐喊，让我们一起为他们点赞，因为他们是明天的主人，是未来的希望！'
        con8 = '河北省赵县的洨河上，有一座世界文明的石拱桥，叫安济桥，又叫赵州桥。'
        # self.handler_mis_sensitive(text=con8)


if __name__ == '__main__':
    run_code = HandlerMisSensitive()
    run_code.run()
