from utils.file_handler import read_sales_data
from utils.file_handler import parse_transactions
from utils.file_handler import validate_and_filter
from utils.api_handler import fetch_all_products, create_product_mapping
from utils.api_handler import enrich_sales_data, save_enriched_data
from utils.report_generator_fun import generate_sales_report

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def main():
   
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1. Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # 2. Parse & clean
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # 3. Display filter options
        regions = sorted(set(t["Region"] for t in transactions))
        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]

        print("\n[3/10] Filter Options Available:")
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        apply_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region = min_amt = max_amt = None
        if apply_filter == "y":
            region = input("Enter region (or press Enter to skip): ").strip() or None
            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amt = float(min_amt) if min_amt else None
            max_amt = float(max_amt) if max_amt else None

        # 4. Validate & filter
        print("\n[4/10] Validating transactions...")
        valid_txns, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amt,
            max_amount=max_amt
        )
        print(f"✓ Valid: {len(valid_txns)} | Invalid: {invalid_count}")

        # 5. Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_txns)
        region_wise_sales(valid_txns)
        top_selling_products(valid_txns)
        customer_analysis(valid_txns)
        daily_sales_trend(valid_txns)
        find_peak_sales_day(valid_txns)
        low_performing_products(valid_txns)
        print("✓ Analysis complete")

        # 6. Fetch API data
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")

        # 7. Enrichment
        print("\n[7/10] Enriching sales data...")
        enriched = enrich_sales_data(valid_txns, product_mapping)
        success = sum(1 for t in enriched if t["API_Match"])
        print(f"✓ Enriched {success}/{len(enriched)} transactions "
              f"({(success / len(enriched)) * 100:.1f}%)")

        # 8. Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # 9. Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_txns, enriched)
        print("✓ Report saved to: output/sales_report.txt")

        # 10. Complete
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n ERROR OCCURRED")
        print(f"Reason: {str(e)}")
        print("Please check input files or configurations.")
        print("=" * 40)


if __name__ == "__main__":
    main()
