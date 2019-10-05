import random
from typing import re


def gen_vcode(length=4):
    return ''.join(random.choices('0123456789', k=length))

OTHER = 0
MAIL = 1
PHONE = 2

def mail_or_phone(text):
    if re.match(r'^[0-9a-z\-._]+@([0-9a-z]+.)+[a-z]+$', text, re.I):
        return MAIL
    elif re.match(r"^1[35678]\d{9}$", text):
        return PHONE
    else:
        return OTHER