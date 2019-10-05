import json
import random
from urllib import parse, request


def send_sms_single(apikey, text, mobile):
    """
    通用接口发短信
    """
    url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8;",
        "Accept": "application/json;charset=utf-8;"
    }
    data = {
        'apikey': apikey,
        'text': text,
        'mobile': mobile
    }

    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)
    content = request.urlopen(req).read().decode()
    json_data = json.loads(content)

    return json_data


def send_sms(apikey, template, mobile):
    vcode = ''.join(random.choices('0123456789', k=4))

    text = template.format(vcode)
    json_data = send_sms_single(apikey, text, mobile)
    print('云片网结果：', json_data)
    if json_data['code'] == 0:
        return True, vcode
    else:
        return False, vcode


if __name__ == '__main__':
    apikey = '9d13289f67041b3713d51df5c6e5e76e'
    template = '【一天拓客】您的验证码是{}。如非本人操作，请忽略本短信。'
    b, vcode = send_sms(apikey, template, '13871343025')
    print(vcode)
