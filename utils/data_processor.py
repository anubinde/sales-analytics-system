# sales analysis

#to calculate total revenue
def calculate_total_revenue(transactions):
    
    total_revenue = 0.0

    for tx in transactions:
        try:
            total_revenue += tx["Quantity"] * tx["UnitPrice"]
        except (KeyError, TypeError):
            # skip transactions with missing or invalid data
            continue

    return round(total_revenue, 2)


# for region wise sales analysis
def region_wise_sales(transactions):
    
    region_stats = {}
    grand_total_sales = 0.0

    for tx in transactions:
        try:
            region = tx["Region"]
            sale_amount = tx["Quantity"] * tx["UnitPrice"]

            grand_total_sales += sale_amount

            if region not in region_stats:
                region_stats[region] = {
                    "total_sales": 0.0,
                    "transaction_count": 0
                }

            region_stats[region]["total_sales"] += sale_amount
            region_stats[region]["transaction_count"] += 1

        except (KeyError, TypeError):
            # skip invalid records
            continue

    #calculate percentage
    for region in region_stats:
        total_sales = region_stats[region]["total_sales"]
        percentage = (total_sales / grand_total_sales) * 100 if grand_total_sales > 0 else 0

        region_stats[region]["percentage"] = round(percentage, 2)
        region_stats[region]["total_sales"] = round(total_sales, 2)

    # sorting
    sorted_region_stats = dict(
        sorted(
            region_stats.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_region_stats

# for top selling products
def top_selling_products(transactions, n=5):

    product_stats = {}

    for tx in transactions:
        try:
            product = tx["ProductName"]
            quantity = tx["Quantity"]
            revenue = quantity * tx["UnitPrice"]

            if product not in product_stats:
                product_stats[product] = {
                    "total_quantity": 0,
                    "total_revenue": 0.0
                }

            product_stats[product]["total_quantity"] += quantity
            product_stats[product]["total_revenue"] += revenue

        except (KeyError, TypeError):
            # skip invalid records
            continue

    #sorting
    sorted_products = sorted(
        product_stats.items(),
        key=lambda item: item[1]["total_quantity"],
        reverse=True
    )

    #to display top N
    top_products = []

    for product, stats in sorted_products[:n]:
        top_products.append((
            product,
            stats["total_quantity"],
            round(stats["total_revenue"], 2)
        ))

    return top_products

#customer analysis

def customer_analysis(transactions):
    
    customer_stats = {}

    
    for tx in transactions:
        try:
            customer_id = tx["CustomerID"]
            product = tx["ProductName"]
            order_value = tx["Quantity"] * tx["UnitPrice"]

            if customer_id not in customer_stats:
                customer_stats[customer_id] = {
                    "total_spent": 0.0,
                    "purchase_count": 0,
                    "products_bought": set()
                }

            customer_stats[customer_id]["total_spent"] += order_value
            customer_stats[customer_id]["purchase_count"] += 1
            customer_stats[customer_id]["products_bought"].add(product)

        except (KeyError, TypeError):
            # skip invalid records
            continue

    # customer calculations
    for customer_id in customer_stats:
        total_spent = customer_stats[customer_id]["total_spent"]
        purchase_count = customer_stats[customer_id]["purchase_count"]

        avg_order_value = total_spent / purchase_count if purchase_count > 0 else 0

        customer_stats[customer_id]["avg_order_value"] = round(avg_order_value, 2)
        customer_stats[customer_id]["total_spent"] = round(total_spent, 2)
        customer_stats[customer_id]["products_bought"] = sorted(
            list(customer_stats[customer_id]["products_bought"])
        )

    # sorting
    sorted_customers = dict(
        sorted(
            customer_stats.items(),
            key=lambda item: item[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customers

#for daily sales  
def daily_sales_trend(transactions):
    
    daily_stats = {}

    for tx in transactions:
        try:
            date = tx["Date"]
            customer_id = tx["CustomerID"]
            revenue = tx["Quantity"] * tx["UnitPrice"]

            if date not in daily_stats:
                daily_stats[date] = {
                    "revenue": 0.0,
                    "transaction_count": 0,
                    "unique_customers": set()
                }

            daily_stats[date]["revenue"] += revenue
            daily_stats[date]["transaction_count"] += 1
            daily_stats[date]["unique_customers"].add(customer_id)

        except (KeyError, TypeError):
            # skip invalid records
            continue

    #formating
    for date in daily_stats:
        daily_stats[date]["revenue"] = round(daily_stats[date]["revenue"], 2)
        daily_stats[date]["unique_customers"] = len(
            daily_stats[date]["unique_customers"]
        )

    #sorting chronologically
    sorted_daily_stats = dict(sorted(daily_stats.items()))

    return sorted_daily_stats

# to find peak sales days 
def find_peak_sales_day(transactions):
    
    daily_summary = {}

    #aggregating
    for tx in transactions:
        try:
            date = tx["Date"]
            revenue = tx["Quantity"] * tx["UnitPrice"]

            if date not in daily_summary:
                daily_summary[date] = {
                    "revenue": 0.0,
                    "transaction_count": 0
                }

            daily_summary[date]["revenue"] += revenue
            daily_summary[date]["transaction_count"] += 1

        except (KeyError, TypeError):
            # skip malformed records
            continue

    if not daily_summary:
        return None, 0.0, 0

    #peak day
    peak_date, peak_data = max(
        daily_summary.items(),
        key=lambda item: item[1]["revenue"]
    )

    return (
        peak_date,
        round(peak_data["revenue"], 2),
        peak_data["transaction_count"]
    )


# to filter out low performing products
def low_performing_products(transactions, threshold=10):
    
    product_stats = {}

    #aggregating
    for tx in transactions:
        try:
            product = tx["ProductName"]
            quantity = tx["Quantity"]
            revenue = quantity * tx["UnitPrice"]

            if product not in product_stats:
                product_stats[product] = {
                    "total_quantity": 0,
                    "total_revenue": 0.0
                }

            product_stats[product]["total_quantity"] += quantity
            product_stats[product]["total_revenue"] += revenue

        except (KeyError, TypeError):
            # skip malformed records
            continue

    # filtering
    low_performers = [
        (
            product,
            stats["total_quantity"],
            round(stats["total_revenue"], 2)
        )
        for product, stats in product_stats.items()
        if stats["total_quantity"] < threshold
    ]

    # sorting
    low_performers.sort(key=lambda x: x[1])

    return low_performers






