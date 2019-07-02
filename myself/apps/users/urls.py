from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^test_view/$', views.TestView.as_view()),
]
