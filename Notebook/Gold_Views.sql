%sql
-- Databricks notebook source
CREATE OR REPLACE VIEW retail_q.retail_gold.dim_customer AS

SELECT
    row_number() OVER (ORDER BY account_name) AS customer_id,
    account_name AS customer_name,
    type AS customer_type,

    billing_city,
    billing_state_province AS billing_state,
    billing_country,

    phone,
    website,

    industry,
    description

FROM retail_q.default.salesforce_bronze

WHERE opportunity_name IS NULL;

-- COMMAND ----------

CREATE OR REPLACE VIEW retail_q.retail_gold.dim_product AS

SELECT
    product_id,
    product_name,
    category,
    subcategory,
    brand,
    unit_price,
    supplier_name,
    launch_date,
    updated_at

FROM retail_q.retail_silver.product_catalog
where is_active=true;

-- COMMAND ----------

CREATE OR REPLACE VIEW retail_q.retail_gold.fact_inventory AS

SELECT
    inventory_id,
    product_id,
    stock_quantity,
    reorder_level,
    inventory_status,
    warehouse_location,
    last_stock_update
FROM retail_q.retail_silver.inventory;

%sql
-- Enriched fact_sales with customer_id for metric view joins
CREATE OR REPLACE VIEW retail_q.retail_gold.fact_sales_enriched AS
SELECT
    f.transaction_id,
    f.opportunity_name,
    f.product_id,
    f.store_id,
    f.quantity,
    f.selling_price,
    f.discount_amount,
    f.transaction_timestamp,
    f.transaction_date,
    f.payment_mode,
    f.sales_channel,
    f.name,
    f.stage_name,
    f.amount,
    c.customer_id
FROM retail_q.retail_gold.fact_sales f
LEFT JOIN retail_q.retail_gold.dim_customer c
    ON f.name = c.customer_name;
