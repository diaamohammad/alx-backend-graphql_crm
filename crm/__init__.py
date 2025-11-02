# هذا الكود ليقرأ الـ "app" المزيف الذي نسخناه
from .celery import app as celery_app

__all__ = ('celery_app',)