import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# الـ URL الخاص بالـ API (افترضناه)
API_URL = "http://localhost:8000/graphql"

# المسارات الخاصة بملفات اللوج
LOG_HEARTBEAT = '/tmp/crm_heartbeat_log.txt'
LOG_STOCK = "/tmp/low_stock_updates_log.txt"

# ==========================================================
# المهمة 2: تسجيل نبضات القلب
# ==========================================================
def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive\n"

    # الجزء الاختياري: التحقق من GraphQL (بيعتمد على الخطوة 2)
    try:
        transport = RequestsHTTPTransport(url=API_URL, verify=True)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("query { hello }") 
        client.execute(query)
        message += f"{timestamp} GraphQL endpoint is responsive.\n"
    except Exception as e:
        message += f"{timestamp} ERROR connecting to GraphQL: {e}\n"

    # كتابة كل شيء إلى الملف
    try:
        with open(LOG_HEARTBEAT, 'a') as f:
            f.write(message)
    except Exception as e:
        print(f"Failed to write to heartbeat log: {e}")

# ==========================================================
# المهمة 3: تحديث المخزون المنخفض
# ==========================================================
def update_low_stock():
    transport = RequestsHTTPTransport(url=API_URL, verify=True)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation_string = """
    mutation UpdateLowStock {
      updateLowStock {
        success
        updatedProducts {
          name
          stock
        }
      }
    }
    """
    mutation = gql(mutation_string)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        result = client.execute(mutation)
        products = result.get('updateLowStock', {}).get('updatedProducts', [])

        with open(LOG_STOCK, 'a') as f:
            if products:
                f.write(f"{timestamp}: Successfully restocked {len(products)} products.\n")
                for prod in products:
                    f.write(f"  - Updated: {prod['name']}, New Stock: {prod['stock']}\n")
            else:
                f.write(f"{timestamp}: No products needed restocking.\n")

    except Exception as e:
        with open(LOG_STOCK, 'a') as f:
            f.write(f"{timestamp}: ERROR running stock update mutation: {e}\n")