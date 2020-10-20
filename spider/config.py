import os
from io import StringIO
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Note:
# 1. dotenv默认会使用US-ASCII编码读取文本文件, 除非在系统环境中设置LC_CTYPE
# 2. 因为env文件中会包含中文, 需要设置系统的LC_CTYPE=zh_CN.UTF-8或者在读取的强制按照utf8编码
with StringIO(open(BASE_DIR + '/.env', encoding='utf-8').read()) as f:
    load_dotenv(stream=f, override=True)


class BaseConfig(object):

    MYSQL_URL = os.getenv('MYSQL_URL') or \
                'mysql+pymysql://root:@127.0.0.1:3306/f_football?charset=utf8'


config = BaseConfig()
