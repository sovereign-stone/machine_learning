import os
from dotenv import load_dotenv

load_dotenv()  # 加载.env文件

# proxy setting
socks5 = os.getenv("PROXY")
proxies = os.getenv("PROXIES")

# redis setting
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_pwd = os.getenv("REDIS_PASSWORD")

# Development ES setting
es_hosts_dev = os.getenv("ES_HOSTS_DEV")
es_name_dev = os.getenv("ES_USERNAME_DEV")
es_pwd_dev = os.getenv("ES_PASSWORD_DEV")

# Product ES setting
es_hosts = os.getenv("ES_HOSTS")
es_name = os.getenv("ES_USERNAME")
es_pwd = os.getenv("ES_PASSWORD")

