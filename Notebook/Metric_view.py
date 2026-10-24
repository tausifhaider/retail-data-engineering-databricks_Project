%sql
ALTER VIEW retail_q.retail_semantic.retail_metrics
AS $$
version: 1.1
source: retail_q.retail_gold.fact_sales_enriched
filter: transaction_date >= '2025-01-01'
comment: Retail sales metrics covering revenue, quantity, discounts, and transaction counts across products, channels, and customers
joins:
  - name: products
    source: retail_q.retail_gold.dim_product
    on: source.product_id = products.product_id
    cardinality: many_to_one
    rely:
      at_most_one_match: true
  - name: calendar
    source: retail_q.retail_gold.dim_calendar
    on: source.transaction_date = calendar.date
    cardinality: many_to_one
    rely:
      at_most_one_match: true
  - name: customers
    source: retail_q.retail_gold.dim_customer
    on: source.customer_id = customers.customer_id
    cardinality: many_to_one
    rely:
      at_most_one_match: true
dimensions:
  - name: product_category
    expr: products.category
    display_name: Product Category
    comment: Product category (Electronics, Fashion, Groceries, etc.)
    synonyms:
      - category
      - product type
  - name: sales_channel
    expr: source.sales_channel
    display_name: Sales Channel
    comment: Channel through which the sale was made
    synonyms:
      - channel
  - name: payment_mode
    expr: source.payment_mode
    display_name: Payment Mode
    comment: Method of payment used for the transaction
    synonyms:
      - payment method
      - payment type
  - name: transaction_month
    expr: DATE_TRUNC('MONTH', source.transaction_date)
    display_name: Transaction Month
    comment: Month of the transaction
    format:
      type: date
      date_format: locale_short_month
    synonyms:
      - month
      - sales month
  - name: customer_type
    expr: customers.customer_type
    display_name: Customer Type
    comment: Type of customer
    synonyms:
      - customer segment
  - name: customer_name
    expr: customers.customer_name
    display_name: Customer Name
    comment: Name of the customer who made the transaction
    synonyms:
      - customer
      - buyer name
  - name: billing_city
    expr: customers.billing_city
    display_name: Customer City
    comment: Billing city of the customer
    synonyms:
      - city
      - customer location
  - name: billing_state
    expr: customers.billing_state
    display_name: Customer State
    comment: Billing state of the customer
    synonyms:
      - state
      - customer region
measures:
  - name: total_revenue
    expr: SUM(source.amount)
    display_name: Total Revenue
    comment: Total sales revenue across all transactions
    format:
      type: currency
      currency_code: INR
      decimal_places:
        type: exact
        places: 2
    synonyms:
      - revenue
      - sales amount
  - name: total_quantity
    expr: SUM(source.quantity)
    display_name: Total Quantity Sold
    comment: Total number of units sold
    format:
      type: number
      decimal_places:
        type: exact
        places: 0
    synonyms:
      - quantity
      - units sold
  - name: transaction_count
    expr: COUNT(*)
    display_name: Transaction Count
    comment: Total number of sales transactions
    format:
      type: number
      decimal_places:
        type: exact
        places: 0
    synonyms:
      - number of transactions
      - order count
  - name: total_discount
    expr: SUM(source.discount_amount)
    display_name: Total Discount
    comment: Total discount amount given across all transactions
    format:
      type: currency
      currency_code: INR
      decimal_places:
        type: exact
        places: 2
    synonyms:
      - discount
  - name: avg_selling_price
    expr: AVG(source.selling_price)
    display_name: Average Selling Price
    comment: Average per-unit selling price across all transactions
    format:
      type: currency
      currency_code: INR
      decimal_places:
        type: exact
        places: 2
    synonyms:
      - average price
      - avg price
$$
