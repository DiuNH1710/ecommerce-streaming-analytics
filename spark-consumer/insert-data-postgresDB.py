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

def insert_csv_to_table (conn, csv_path, table_name, columns, sleep_time = 1): 
    
      placeholders = ','.join(['%s']*len(columns))
      cols_formatted = ','.join(columns)
      insert_query = sql.SQL(
            f"INSERT INTO {table_name} ({cols_formatted}) VALUES({placeholders})"
      )
      
      with open(csv_path, mode='r', encoding='utf-8') as file: 
            reader = csv.reader(file)
            headers = next(reader)
            
            for row in reader:
                  row = [None if r == '' else r for r in row] 
                  try: 
                        with conn.cursor ()  as cur: 
                              cur.execute(insert_query, row)
                              conn.commit()
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

      threads.append(threading.Thread(target=insert_csv_to_table, args=(
            conn,
            "../archive/sale_report.csv",
            "sale_report",
            ["sku_code", "design_no", "stock", "category", "size", "color"],
            1
      )))

      threads.append(threading.Thread(target=insert_csv_to_table, args=(
            conn,
            "../archive/pnl_march_2021.csv",
            "pnl_march_2021",
            [
                  "sku", "style_id", "catalog", "category", "weight", "tp1", "tp2",
                  "mrp_old", "final_mrp_old", "ajio_mrp", "amazon_mrp",
                  "amazon_fba_mrp", "flipkart_mrp", "limeroad_mrp",
                  "myntra_mrp", "paytm_mrp", "snapdeal_mrp"
            ],
            1
      )))

      threads.append(threading.Thread(target=insert_csv_to_table, args=(
            conn,
            "../archive/may_2022.csv",
            "may_2022",
            [
                  "sku", "style_id", "catalog", "category", "weight", "tp",
                  "mrp_old", "final_mrp_old", "ajio_mrp", "amazon_mrp",
                  "amazon_fba_mrp", "flipkart_mrp", "limeroad_mrp",
                  "myntra_mrp", "paytm_mrp", "snapdeal_mrp"
            ],
            1
      )))

      threads.append(threading.Thread(target=insert_csv_to_table, args=(
            conn,
            "../archive/amazon_sale_report.csv",
            "amazon_sale_report",
            [
                  "order_id", "date", "status", "fulfilment", "sales_channel",
                  "ship_service_level", "style", "sku", "category", "size", "asin",
                  "courier_status", "qty", "currency", "amount", "ship_city",
                  "ship_state", "ship_postal_code", "ship_country", "promotion_ids",
                  "b2b", "fulfilled_by"
            ],
            1
      )))

      threads.append(threading.Thread(target=insert_csv_to_table, args=(
            conn,
            "../archive/international_sale_report.csv",
            "international_sale_report",
            [
                  "style", "sku", "size", "date", "months", "customer", "pcs", "rate", "gross_amt"
            ],
            1
      )))

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