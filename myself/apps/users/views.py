from django.http import HttpResponse
from django.views import View


class TestView(View):
    def get(self, request):
        # 测试session的redis配置
        # request.session['username'] = 'zs'

        username = request.session.get('username', None)

        return HttpResponse('TestView')
