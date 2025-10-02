import mysql.connector


def write_to_mysql(batch_df, epoch_id):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='ecommerce_db'
    )
    cursor = conn.cursor()
    pandas_df = batch_df.toPandas()

    for _, row in pandas_df.iterrows():
        cursor.execute("""
            REPLACE INTO products_per_category (category, tong_san_pham, updated_at)
            VALUES (%s, %s, NOW());
        """, (row['category'], int(row['tong_san_pham'])))

    conn.commit()
    cursor.close()
    conn.close()
