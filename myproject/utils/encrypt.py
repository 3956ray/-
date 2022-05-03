import hashlib
from django.conf import settings

# md5加密函数
def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # md5 盐 调用django生成的密钥
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
