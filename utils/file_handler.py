#data file handling, processing, validating and filtering

def read_sales_data(filename):
    
    encodings = ["utf-8", "latin-1", "cp1252"]
    raw_lines = []

    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = file.readlines()

                # skip header and remove empty lines
                for line in lines[1:]:
                    line = line.strip()
                    if line:
                        raw_lines.append(line)

            print(f"file read successfully using encoding: {encoding}")
            return raw_lines

        except UnicodeDecodeError:
            #next encoding
            continue

        except FileNotFoundError:
            print(f"error: File not found -> {filename}")
            return []

        except Exception as e:
            print(f"unexpected error while reading file: {e}")
            return []

    print("error: unable to read file with supported encodings.")
    return []

def parse_transactions(raw_lines):
    
    parsed_records = []
    expected_fields = 8

    for line in raw_lines:
        try:
            parts = line.split("|")

            # skip rows that has incorrect number of fields
            if len(parts) != expected_fields:
                continue

            transaction_id = parts[0].strip()
            date = parts[1].strip()
            product_id = parts[2].strip()

            # remove commas from productname column
            product_name = parts[3].replace(",", "").strip()

            # converting numeric features
            quantity = int(parts[4].replace(",", "").strip())
            unit_price = float(parts[5].replace(",", "").strip())

            customer_id = parts[6].strip()
            region = parts[7].strip()

            parsed_records.append({
                "TransactionID": transaction_id,
                "Date": date,
                "ProductID": product_id,
                "ProductName": product_name,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "CustomerID": customer_id,
                "Region": region
            })

        except ValueError:
            # to skip invalid numeric conversion rows
            continue
        except Exception:
            # to skip unexpected malformed rows
            continue

    return parsed_records

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    
    required_fields = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region"
    ]

    total_input = len(transactions)
    invalid_count = 0
    valid_transactions = []

    # VAIDATION
    for tx in transactions:
        try:
            # first check required fields
            if not all(field in tx for field in required_fields):
                invalid_count += 1
                continue

            # field level validations
            if not tx["TransactionID"].startswith("T"):
                invalid_count += 1
                continue

            if not tx["ProductID"].startswith("P"):
                invalid_count += 1
                continue

            if not tx["CustomerID"].startswith("C"):
                invalid_count += 1
                continue

            if tx["Quantity"] <= 0 or tx["UnitPrice"] <= 0:
                invalid_count += 1
                continue

            valid_transactions.append(tx)

        except Exception:
            invalid_count += 1

    # METADATA
    regions = sorted({tx["Region"] for tx in valid_transactions})
    amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in valid_transactions]

    print("available regions :", regions)
    print("transaction amount range :", min(amounts, default=0), "-", max(amounts, default=0))

    filtered_by_region = 0
    filtered_by_amount = 0

    # REGION FILTER
    if region:
        before = len(valid_transactions)
        valid_transactions = [
            tx for tx in valid_transactions if tx["Region"] == region
        ]
        filtered_by_region = before - len(valid_transactions)
        print(f"after region filter ({region}) :", len(valid_transactions))

    # AMOUNT FILTER
    if min_amount is not None or max_amount is not None:
        before = len(valid_transactions)

        def amount_in_range(tx):
            amount = tx["Quantity"] * tx["UnitPrice"]
            if min_amount is not None and amount < min_amount:
                return False
            if max_amount is not None and amount > max_amount:
                return False
            return True

        valid_transactions = [
            tx for tx in valid_transactions if amount_in_range(tx)
        ]

        filtered_by_amount = before - len(valid_transactions)
        print("after amount filter :", len(valid_transactions))

    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary
