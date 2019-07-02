from django.conf.urls import url

from verifications import views

urlpatterns = [
    url(r'^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCode.as_view())
]
