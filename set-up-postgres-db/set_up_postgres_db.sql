
CREATE TABLE IF NOT EXISTS import_state (
    table_name TEXT PRIMARY KEY,
    last_row_imported INT DEFAULT -1
);

-- 1. Sale Report

CREATE TABLE sale_report (
    id SERIAL PRIMARY KEY,
    sku_code VARCHAR(50),
    design_no VARCHAR(50),
    stock NUMERIC,
    category VARCHAR(100),
    size VARCHAR(20),
    color VARCHAR(50)
);

-- 2. P & L March 2021
CREATE TABLE pnl_march_2021 (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50),
    style_id VARCHAR(50),
    catalog VARCHAR(100),
    category VARCHAR(50),
    weight NUMERIC,
    tp1 NUMERIC,
    tp2 NUMERIC,
    mrp_old NUMERIC,
    final_mrp_old NUMERIC,
    ajio_mrp NUMERIC,
    amazon_mrp NUMERIC,
    amazon_fba_mrp NUMERIC,
    flipkart_mrp NUMERIC,
    limeroad_mrp NUMERIC,
    myntra_mrp NUMERIC,
    paytm_mrp NUMERIC,
    snapdeal_mrp NUMERIC
);

-- 3. May 2022
CREATE TABLE may_2022 (
      id SERIAL PRIMARY KEY,
    sku VARCHAR(50),
    style_id VARCHAR(50),
    catalog VARCHAR(100),
    category VARCHAR(100),
    weight NUMERIC,
    tp NUMERIC,
    mrp_old NUMERIC,
    final_mrp_old NUMERIC,
    ajio_mrp NUMERIC,
    amazon_mrp NUMERIC,
    amazon_fba_mrp NUMERIC,
    flipkart_mrp NUMERIC,
    limeroad_mrp NUMERIC,
    myntra_mrp NUMERIC,
    paytm_mrp NUMERIC,
    snapdeal_mrp NUMERIC
);

-- 4. Amazon Sale Report

CREATE TABLE amazon_sale_report (
      id SERIAL PRIMARY KEY,
    order_id VARCHAR(50),
    date DATE,
    status VARCHAR(100),
    fulfilment VARCHAR(50),
    sales_channel VARCHAR(50),
    ship_service_level VARCHAR(100),
    style VARCHAR(100),
    sku VARCHAR(50),
    category VARCHAR(100),
    size VARCHAR(10),
    asin VARCHAR(20),
    courier_status VARCHAR(50),
    qty INT,
    currency VARCHAR(10),
    amount NUMERIC(10,2),
    ship_city VARCHAR(50),
    ship_state VARCHAR(50),
    ship_postal_code VARCHAR(20),
    ship_country VARCHAR(10),
    promotion_ids TEXT,
    b2b BOOLEAN,
    fulfilled_by VARCHAR(50)

);

-- 5. International_sale_report

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

