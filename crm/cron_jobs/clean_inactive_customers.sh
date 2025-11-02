#!/bin/bash

# === !! غيّر هذه المسارات !! ===
PROJECT_DIR="/path/to/your/project/alx-backend-graphql_crm"
VENV_PATH="/path/to/your/project/alx-backend-graphql_crm/venv/bin/activate"
# ===============================

LOG_FILE="/tmp/customer_cleanup_log.txt"

# تفعيل البيئة الافتراضية
source $VENV_PATH

# الانتقال إلى مجلد المشروع
cd $PROJECT_DIR

# أمر البايثون
PYTHON_COMMAND="
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer # تأكد من مسار المودل
import datetime

one_year_ago = timezone.now() - timedelta(days=365)

# إيجاد ID العملاء الذين لديهم طلبات في آخر 365 يوم
recent_customer_ids = Customer.objects.filter(
    orders__created_at__gte=one_year_ago
).values_list('id', flat=True).distinct()

# حذف كل العملاء الذين *ليسوا* في القائمة السابقة
inactive_customers_qs = Customer.objects.exclude(id__in=recent_customer_ids)
count = inactive_customers_qs.count()
inactive_customers_qs.delete()

timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f'{timestamp}: Deleted {count} inactive customers (no orders in the past year).')
"

# تشغيل الأمر وتسجيل المخرجات
python manage.py shell -c "$PYTHON_COMMAND" >> $LOG_FILE 2>&1