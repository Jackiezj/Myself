import random

from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from myself.libs.captcha.captcha import captcha
from verifications.constants import IMAGE_CODE_REDIS_EXPIRES, SMS_CODE_REDIS_EXPIRES
from verifications.serializer import ImageCodeCheckSerializer


class ImageCode(APIView):
    """
    生成图片验证码
    """

    def get(self, request, image_code_id):
        """
        生成图片验证码保存cache并返回
        :param request:
        :param image_code_id:
        :return:
        """
        # 生成图片验证码
        code, image = captcha.generate_captcha()

        # 保存redis
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex("image_code_%s" % image_code_id, IMAGE_CODE_REDIS_EXPIRES, code)

        return HttpResponse(image, content_type='image/jpg')


class SMSCode(GenericAPIView):
    """发送验证码"""

    serializer_class = ImageCodeCheckSerializer

    def get(self, request, mobile):
        """
        发送短信验证码
        :param request:
        :param mobile: 手机号
        :return:
        """
        # 序列化器实现校验参数
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 发送短信验证码
        sms_code = "%06d" % random.randint(0, 999999)
        redis_conn = get_redis_connection('verify_codes')
        pl = redis_conn.pipeline()
        pl.setex('sms_code_%s' % mobile, SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, SMS_CODE_REDIS_EXPIRES, 1)
        pl.execute()
        # TODO 异步发送短信验证码

        return Response({'message': 'OK'})



