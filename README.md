# sales-analytics-system

A Python-based Sales Analytics Pipeline that reads sales transactions, performs data cleaning, analysis, API enrichment, and generates a comprehensive report.
 ##  Project Structure
 sales-analytics-system/
├── README.md
├── main.py
 |———main.ipynb
├── utils/
│ ├── file_handler.py
│ ├── data_processor.py
│ └── api_handler.py
├── data/
│ └── sales_data.txt
├── output/
    |____sales_report.txt
└── requirements.txt

---

## Features

- Reads and cleans sales transaction data
- Validates and filters data by region and transaction amount
- Calculates:
  - Total revenue
  - Region-wise sales
  - Top-selling products
  - Customer purchase analysis
  - Daily sales trend
  - Peak sales day
  - Low-performing products
- Enriches transaction data with product info from DummyJSON API
- Saves enriched data to `data/enriched_sales_data.txt`
- Generates a detailed text report: `output/sales_report.txt`

---

## Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd sales-analytics-system

How to Run

Ensure sales_data.txt is in the data/ folder.

Run the main pipeline:

python3 main.py


Output files will be generated:

Enriched data: data/enriched_sales_data.txt

Sales report: output/sales_report.txt
