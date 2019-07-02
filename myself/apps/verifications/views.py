from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.views import APIView

from myself.libs.captcha.captcha import captcha
from verifications.constants import IMAGE_CODE_REDIS_EXPIRES


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