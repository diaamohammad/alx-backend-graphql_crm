# إعداد وتشغيل Celery للتقارير

هذا الدليل يشرح كيفية إعداد وتشغيل Celery و Celery Beat لجدولة المهام.

## 1. تثبيت المتطلبات الأساسية (Redis)

نحن نستخدم Redis كوسيط (Broker). قم بتثبيته وتشغيله (داخل WSL):

```bash
sudo apt update
sudo apt install redis-server
sudo service redis-server start