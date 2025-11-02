import os
from celery import Celery

# اضبط إعدادات جانغو الافتراضية لبرنامج 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config') # اسم المشروع

# استخدم 'config' كـ namespace لكل إعدادات Celery
# هذا يعني أن كل إعدادات Celery يجب أن تبدأ بـ CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# اكتشف ملفات tasks.py داخل كل تطبيقات جانغو المسجلة
app.autodiscover_tasks()