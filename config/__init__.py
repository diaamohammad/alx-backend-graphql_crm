# هذا الكود يضمن تحميل التطبيق عند بدء تشغيل جانغو
from .celery import app as celery_app

__all__ = ('celery_app',)