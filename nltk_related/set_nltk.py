import nltk


def nltk_download():
    nltk.set_proxy('http://127.0.0.1:58591')  # 设置代理，如果需要的话
    nltk.download('all', download_dir='/home/soc/nltk_data', quiet=False, raise_on_error=True)


def test():
    from nltk.corpus import brown
    words = brown.words()
    print(words)


# nltk_download()
