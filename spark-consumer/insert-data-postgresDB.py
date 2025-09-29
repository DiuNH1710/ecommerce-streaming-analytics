import time
import csv
import psycopg2
from psycopg2 import sql 
import threading


# Database config 
conn_details = {
      'dbname': "ecommerce", 
      'user': 'postgres', 
      'password': 'postgres', 
      'host': 'postgres', 
      'port': '5432'
}

# Connect to postgresql

def connect_to_db(): 
      try: 
            conn = psycopg2.connect(**conn_details)
            print("✅ Connected to PostgreSQL")
            return conn
      except Exception as e : 
            print(f"❌ Error connecting to the database: {e}")
            return None

# CSV -> DB Insert Function


#     Insert từng dòng từ CSV vào bảng Postgres
#     - csv_path: đường dẫn file CSV
#     - table_name: tên bảng trong Postgres
#     - columns: list tên cột tương ứng trong bảng
#     - sleep_time: thời gian chờ giữa mỗi insert (giả lập streaming) 

def get_start_row(conn, table_name):
    with conn.cursor() as cur:
        cur.execute("SELECT last_row_imported FROM import_state WHERE table_name=%s", (table_name,))
        res = cur.fetchone()
        return res[0] + 1 if res else 0

def update_last_row(conn, table_name, row_idx):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO import_state(table_name, last_row_imported)
            VALUES(%s, %s)
            ON CONFLICT(table_name) DO UPDATE
            SET last_row_imported = EXCLUDED.last_row_imported
        """, (table_name, row_idx))
        conn.commit()

def insert_csv_to_table(conn, csv_path, table_name, columns, sleep_time=1): 
    placeholders = ','.join(['%s'] * len(columns))
    cols_formatted = ','.join(columns)
    insert_query = f"INSERT INTO {table_name} ({cols_formatted}) VALUES({placeholders})"
    
    with open(csv_path, mode='r', encoding='utf-8') as file: 
        reader = csv.reader(file)
        headers = next(reader)
        
        start_row = get_start_row(conn, table_name)

        for i, row in enumerate(reader):
            if i < start_row:
                  continue  

            # ⚠️ Bỏ cột đầu tiên nếu là index
            row = row[1:]  

            # Chuyển chuỗi rỗng thành None
            row = [None if r == '' else r for r in row]
            print(f"[DEBUG] Row length after removing index: {len(row)} | Expected: {len(columns)}")
            print("[DEBUG] Row data:", row)
            
            try:
                with conn.cursor() as cur:
                    cur.execute(insert_query, row)
                    conn.commit()
                update_last_row(conn, table_name, i)
                print(f"✅ Inserted row into {table_name}: {row}")
                time.sleep(sleep_time)
            except Exception as e:
                print(f"❌ Error inserting row into {table_name}: {e}")
                conn.rollback()

def main():
      conn = connect_to_db()
      if not conn:
            return

      threads = []

      # threads.append(threading.Thread(target=insert_csv_to_table, args=(
      #       conn,
      #       "/app/archive/sale_report.csv",
      #       "sale_report",
      #       ["sku_code", "design_no", "stock", "category", "size", "color"],
      #       1
      # )))

      # threads.append(threading.Thread(target=insert_csv_to_table, args=(
      #       conn,
      #       "/app/archive/pnl_march_2021.csv",
      #       "pnl_march_2021",
      #       [
      #             "sku", "style_id", "catalog", "category", "weight", "tp1", "tp2",
      #             "mrp_old", "final_mrp_old", "ajio_mrp", "amazon_mrp",
      #             "amazon_fba_mrp", "flipkart_mrp", "limeroad_mrp",
      #             "myntra_mrp", "paytm_mrp", "snapdeal_mrp"
      #       ],
      #       1
      # )))

      threads.append(threading.Thread(target=insert_csv_to_table, args=(
            conn,
            "/app/archive/may_2022.csv",
            "may_2022",
            [
                  "sku", "style_id", "catalog", "category", "weight", "tp",
                  "mrp_old", "final_mrp_old", "ajio_mrp", "amazon_mrp",
                  "amazon_fba_mrp", "flipkart_mrp", "limeroad_mrp",
                  "myntra_mrp", "paytm_mrp", "snapdeal_mrp"
            ],
            1
      )))

      # threads.append(threading.Thread(target=insert_csv_to_table, args=(
      #       conn,
      #       "/app/archive/amazon_sale_report.csv",
      #       "amazon_sale_report",
      #       [
      #             "order_id", "date", "status", "fulfilment", "sales_channel",
      #             "ship_service_level", "style", "sku", "category", "size", "asin",
      #             "courier_status", "qty", "currency", "amount", "ship_city",
      #             "ship_state", "ship_postal_code", "ship_country", "promotion_ids",
      #             "b2b", "fulfilled_by"
      #       ],
      #       1
      # )))

      # threads.append(threading.Thread(target=insert_csv_to_table, args=(
      #       conn,
      #       "/app/archive/international_sale_report.csv",
      #       "international_sale_report",
      #       [
      #             "style", "sku", "size", "date", "months", "customer", "pcs", "rate", "gross_amt"
      #       ],
      #       1
      # )))

      # 🚀 Start all threads
      for t in threads:
            t.start()

      # ⏳ Wait for all to complete
      for t in threads:
            t.join()

      conn.close()
      print("🎉 All CSV files imported successfully in parallel!")

if __name__ == "__main__":
      main()