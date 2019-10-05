from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import time


# Create your views here.
from common import string_helper, mail_helper
from common.mail_helper import send_vcode
from common.yunpian import send_sms


def register(request):
    if request.method == 'POST':
        return HttpResponse('注册成功！')
    else:
        return render(request, 'vcode_app/register.html')


def send_vcode(request):
    username = request.POST.get('username')

    register_vcode_time = request.session.get('register_vcode_time')
    now_time = time.time()

    if register_vcode_time and now_time < register_vcode_time + settings.MAIL_INTERVAL:
        return JsonResponse({'msg': f'{settings.MAIL_INTERVAL}秒之内，不能重复发送验证码'})
    else:

        typ = string_helper.mail_or_phone(username)

        if typ == string_helper.OTHER:
            return JsonResponse({'ok': 0, 'msg': '账号不是邮箱，也不是手机号'})
        else:
            if typ == string_helper.MAIL:
                vcode = mail_helper.send_vcode(settings.MAIL_SMTP_SERVER,
                           settings.MAIL_FROM_ADDR,
                           settings.MAIL_PASSWORD,
                           username)
                resp = {'ok': 1, 'msg': '验证码已经发送，请查阅邮箱！'}
            else:
                # typ == string_helper.PHONE:
                b, vcode = send_sms(settings.YUNPIAN_APIKEY, settings.YUNPIAN_TEMPLATE, username)
                resp = {'ok': 1, 'msg': '验证码已经发送，请查看手机！'}

            request.session['register_username'] = username
            request.session['register_vcode'] = vcode
            request.session['register_vcode_time'] = time.time()

            return JsonResponse(resp)


def validate_vcode(request):
    register_username = request.session.get('register_username')
    username = request.POST.get('username')

    if register_username and register_username == username:
        now_time = time.time()
        register_vcode_time = request.session.get('register_vcode_time')

        if register_vcode_time and now_time <= register_vcode_time + settings.MAIL_EXPIRE:
            vcode = request.POST.get('vcode')
            register_vcode = request.session.get('register_vcode')

            if register_vcode and register_vcode == vcode:
                resp = {'ok': 1, 'msg': '验证码验证正确！'}
            else:
                resp = {'ok': 0, 'msg': '验证码错误！'}
        else:
            resp = {'ok': 0, 'msg': '验证码已经过期，请重新获取！'}
    else:
        resp = {'ok': 0, 'msg': '该账号还没有获取验证码！'}

    return JsonResponse(resp)


