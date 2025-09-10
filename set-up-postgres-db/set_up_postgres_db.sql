

-- 1. Cloud warehouse compersion chart

CREATE TABLE cloud_warehouse_comparison (
      id SERIAL PRIMARY KEY,
      shiprocket NUMERIC,
      increff NUMERIC
);

-- 2. Sale Report

CREATE TABLE sale_report (
      id SERIAL PRIMARY KEY,
      sku_code VARCHAR(255),
      design_no VARCHAR(255),
      stock INT,
      category VARCHAR(255),
      size VARCHAR(50),
      color VARCHAR(100)
);

-- 3. P & L March 2021
CREATE TABLE pnl_march_2021 (
      id SERIAL PRIMARY KEY,
      category VARCHAR(255),
      sku VARCHAR(255),
      catalog VARCHAR(255), 
      weight INT,
      tp1 INT, 
      tp2 INT, 
      mrp_old INT, 
      final_mrp_old INT,
      ajio_mrp INT,
      amazon_mrp INT,
      amazon_fba_mrp INT,
      flipkart_mrp INT,
      limeroad_mrp INT,
      myntra_mrp INT,
      paytm_mrp INT,
      snapdeal_mrp INT,
);

-- 4. May 2022
CREATE TABLE may_2022 (
      id SERIAL PRIMARY KEY,
      sku VARCHAR(255),
      catalog VARCHAR(255), 
      category VARCHAR(255),
      weight INT, 
      mrp_old INT, 
      final_mrp_old INT,
      ajio_mrp INT,
      amazon_mrp INT,
      amazon_fba_mrp INT,
      flipkart_mrp INT,
      limeroad_mrp INT,
      myntra_mrp INT,
      paytm_mrp INT,
      snapdeal_mrp INT,
      tp1_tp2_mrp_old INT
);

-- 5. Amazon Sale Report

CREATE TABLE amazon_sale_report (
      id SERIAL PRIMARY KEY,
      category VARCHAR(255),
      size VARCHAR(50),
      date DATE, 
      status VARCHAR(100),
      fulfilment VARCHAR(100), 
      style VARCHAR(255), 
      sku VARCHAR(255),
      asin VARCHAR(100),
      courier_status VARCHAR(100),
      qty INT,
      amount NUMERIC, 
      b2b BOOLEAN, 
      currency VARCHAR(50)

);

-- 6. International_sale_report

CREATE TABLE International_sale_report(
      id SERIAL PRIMARY KEY, 
      style VARCHAR(255),
      sku VARCHAR(255),
      size VARCHAR(50),
      date DATE,
      months VARCHAR(50), 
      customer VARCHAR(255),
      pcs INT, 
      rate NUMERIC, 
      gross_amt NUMERIC
);

-- 7. Expense IIGF
CREATE TABLE expense_iigf (
      id SERIAL PRIMARY KEY,
      receipt_amount NUMERIC
);