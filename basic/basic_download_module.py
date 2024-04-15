from transformers import T5Model
from datasets import load_dataset
from huggingface_hub import hf_hub_download
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

path = '/home/soc/.pycorrector/datasets'
model_name = 'shibing624/mengzi-t5-base-chinese-correction'
proxies = {"http": "http://127.0.0.1:58591", "https": "http://127.0.0.1:58591"}


def one():
    # 第一种下载模型方法
    model = T5Model.from_pretrained(path, local_files_only=True, proxies=proxies)
    model.save_pretrained(path)


def two(name=None, url=None):
    # 数据集名称或者 Hugging Face 数据集的 URL
    if name:
        dataset_ = name
    # 数据集的 URL
    elif url:
        dataset_ = url
    else:
        return 'ERROR'
    # 加载数据集
    dataset = load_dataset(dataset_, download_config={"proxies": proxies})
    # 打印数据集信息
    print(dataset)


def three():
    # 第三种下载模型方法
    tokenizer = AutoTokenizer.from_pretrained("shibing624/mengzi-t5-base-chinese-correction")
    model = AutoModelForSeq2SeqLM.from_pretrained("shibing624/mengzi-t5-base-chinese-correction")

    tokenizer.save_pretrained(path)
    model.save_pretrained(path)


def four():
    # 第四种下载模型方法
    hf_hub_download(repo_id="shibing624/mengzi-t5-base-chinese-correction",
                    filename="config.json", cache_dir=path, proxies=proxies)


def five():
    # 第五种下载模型方法
    # 对于需要登录的模型，还需要两行额外代码
    # import huggingface_hub
    # huggingface_hub.login("HF_TOKEN")
    snapshot_download(
        repo_id=model_name,
        local_dir=path,
        proxies=proxies,
        max_workers=8,
        resume_download=True
    )


# one()
# two()
# three()
# four()
five()