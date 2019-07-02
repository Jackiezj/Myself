from celery import Celery

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'myself.settings.dev'

celery_app = Celery('myself')

celery_app.config_from_object("celery_tasks.config")

celery_app.autodiscover_tasks(['celery_tasks.sms'])
