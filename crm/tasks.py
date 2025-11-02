from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime

API_URL = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/crm_report_log.txt"

@shared_task
def generate_crm_report():
    # 1. إعداد الـ Client
    transport = RequestsHTTPTransport(url=API_URL, verify=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # 2. الاستعلام (Query)
    query_string = """
    query GetReportStats {
      totalCustomers
      totalOrders
      totalRevenue
    }
    """
    query = gql(query_string)

    try:
        # 3. تنفيذ الاستعلام
        # (ملاحظة: هذا يتطلب أن سيرفر جانغو يكون شغال!)
        result = client.execute(query)

        customers = result.get('totalCustomers', 0)
        orders = result.get('totalOrders', 0)
        revenue = result.get('totalRevenue', 0)

        # 4. كتابة التقرير
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_line = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue.\n"

        with open(LOG_FILE, 'a') as f:
            f.write(report_line)

        return report_line

    except Exception as e:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_line = f"{timestamp} - ERROR generating report: {e}\n"
        with open(LOG_FILE, 'a') as f:
            f.write(error_line)
        return str(e)