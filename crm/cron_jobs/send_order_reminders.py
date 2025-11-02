import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
API_URL = "http://localhost:8000/graphql"

def log_message(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp}: {message}\n")

def fetch_recent_orders():
    transport = RequestsHTTPTransport(url=API_URL, verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()

    # عدّل الاستعلام بناءً على الـ Schema لديك
    query_string = """
    query GetRecentOrders($dateFilter: DateTime) {
      orders(orderDate_gte: $dateFilter) {
        id
        customer {
          email
        }
      }
    }
    """
    query = gql(query_string)
    params = {"dateFilter": seven_days_ago}

    try:
        result = client.execute(query, variable_values=params)
        return result.get('orders', [])
    except Exception as e:
        log_message(f"Error querying GraphQL: {e}")
        return []

if __name__ == "__main__":
    print("Starting order reminder processing...")
    orders = fetch_recent_orders()

    if orders:
        for order in orders:
            order_id = order.get('id')
            customer_email = order.get('customer', {}).get('email', 'N/A')
            log_message(f"Reminder Sent: Order ID: {order_id}, Customer: {customer_email}")

    log_message("Order reminders processing finished.")
    print("Order reminders processed!")