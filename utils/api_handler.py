import requests
import os

def fetch_all_products():
    
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)

        # to check if request got successful
        if response.status_code == 200:
            data = response.json()
            products = data.get("products", [])

            cleaned_products = []

            for product in products:
                cleaned_products.append({
                    "id": product.get("id"),
                    "title": product.get("title"),
                    "category": product.get("category"),
                    "brand": product.get("brand"),
                    "price": product.get("price"),
                    "rating": product.get("rating")
                })

            print(f"successfully fetched {len(cleaned_products)} products")
            return cleaned_products

        else:
            print(f"API failed with status code: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"connection error occurred: {e}")
        return []

# to create product mapping

def create_product_mapping(api_products):
    
    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping

#enriching data

import os

def enrich_sales_data(transactions, product_mapping):

    enriched_transactions = []

    # to make sure output directory exists
    os.makedirs("data", exist_ok=True)

    output_file = "data/enriched_sales_data.txt"

    # to define header for output file
    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|"
        "API_Category|API_Brand|API_Rating|API_Match\n"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header)

        for txn in transactions:
            try:
                # to extract numeric product ID (P101 -> 101)
                product_id_str = txn.get("ProductID", "")
                numeric_id = int("".join(filter(str.isdigit, product_id_str)))

                api_data = product_mapping.get(numeric_id)

                if api_data:
                    txn["API_Category"] = api_data.get("category")
                    txn["API_Brand"] = api_data.get("brand")
                    txn["API_Rating"] = api_data.get("rating")
                    txn["API_Match"] = True
                else:
                    txn["API_Category"] = None
                    txn["API_Brand"] = None
                    txn["API_Rating"] = None
                    txn["API_Match"] = False

            except Exception:
                txn["API_Category"] = None
                txn["API_Brand"] = None
                txn["API_Rating"] = None
                txn["API_Match"] = False

            enriched_transactions.append(txn)

            # to write enriched transaction to file
            line = (
                f"{txn.get('TransactionID')}|{txn.get('Date')}|{txn.get('ProductID')}|"
                f"{txn.get('ProductName')}|{txn.get('Quantity')}|{txn.get('UnitPrice')}|"
                f"{txn.get('CustomerID')}|{txn.get('Region')}|"
                f"{txn.get('API_Category')}|{txn.get('API_Brand')}|"
                f"{txn.get('API_Rating')}|{txn.get('API_Match')}\n"
            )

            f.write(line)

    print(f"enriched sales data saved to {output_file}")

    return enriched_transactions

# to save enriched data

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
   

    # to ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|"
        "API_Category|API_Brand|API_Rating|API_Match\n"
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write(header)

        for txn in enriched_transactions:
            # replacing None with empty string
            def safe(value):
                return "" if value is None else str(value)

            line = (
                f"{safe(txn.get('TransactionID'))}|"
                f"{safe(txn.get('Date'))}|"
                f"{safe(txn.get('ProductID'))}|"
                f"{safe(txn.get('ProductName'))}|"
                f"{safe(txn.get('Quantity'))}|"
                f"{safe(txn.get('UnitPrice'))}|"
                f"{safe(txn.get('CustomerID'))}|"
                f"{safe(txn.get('Region'))}|"
                f"{safe(txn.get('API_Category'))}|"
                f"{safe(txn.get('API_Brand'))}|"
                f"{safe(txn.get('API_Rating'))}|"
                f"{safe(txn.get('API_Match'))}\n"
            )

            file.write(line)

    print(f"enriched data successfully saved to {filename}")


