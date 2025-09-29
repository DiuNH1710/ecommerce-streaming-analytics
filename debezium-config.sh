#!/bin/bash

# Debezium REST API
DEBEZIUM_URL="http://localhost:8083/connectors"

# Function to create connector for a table
create_connector() {
  local connector_name=$1
  local table_name=$2

  curl -X POST -H "Content-Type: application/json" $DEBEZIUM_URL --data "{
    \"name\": \"$connector_name\",
    \"config\": {
      \"connector.class\": \"io.debezium.connector.postgresql.PostgresConnector\",
      \"plugin.name\": \"pgoutput\",
      \"database.hostname\": \"postgres\",
      \"database.port\": \"5432\",
      \"database.user\": \"postgres\",
      \"database.password\": \"postgres\",
      \"database.dbname\": \"ecommerce\",
      \"database.server.name\": \"postgres\",
      \"table.include.list\": \"public.$table_name\",
      \"topic.prefix\": \"cdc\",
      \"decimal.handling.mode\": \"string\"
    }
  }"
  echo -e "\nConnector $connector_name created for table $table_name"
}


# 1. Sale report
create_connector "sale_report_conn" "sale_report"

# 2. P & L March 2021
create_connector "pnl_march_2021_conn" "pnl_march_2021"

# 3. May 2022
create_connector "may_2022_conn" "may_2022"

# 4. Amazon Sale Report
create_connector "amazon_sale_report_conn" "amazon_sale_report"

# 5. International Sale Report
create_connector "international_sale_report_conn" "international_sale_report"

