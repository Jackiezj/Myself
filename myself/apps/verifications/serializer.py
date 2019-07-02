from django_redis import get_redis_connection
from rest_framework import serializers


class ImageCodeCheckSerializer(serializers.Serializer):
    """校验图片验证码序列化器"""
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        # 获取查询参数
        image_code_id = attrs['image_code_id']
        text = attrs['text']
        # 获取url路由参数
        mobile = self.context['view'].kwargs['mobile']

        # 校验参数
        redis_conn = get_redis_connection('verify_codes')
        real_image_code = redis_conn.get("image_code_%s" % image_code_id)
        if not real_image_code:
            raise serializers.ValidationError('image verification code does not exist')
        redis_conn.delete("image_code_%s" % image_code_id)
        if real_image_code.decode().lower() != text.lower():
            raise serializers.ValidationError('image verification code error')

        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            raise serializers.ValidationError('requesting too frequently')
        return attrs
