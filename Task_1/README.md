# Data Analyst Internship - Task 1: Data Cleaning & Preprocessing

## 🎯 Project Objective
This project automates the process of cleaning and fixing a messy sales dataset (`nigeria_messy_sales_dataset.csv`) using Python and Pandas. The script transforms inconsistent and broken data into a reliable, structured file ready for professional analysis.

## 🛠️ Data Issues Fixed
*   **Column Headers:** Fixed spacing errors and turned headers into standard lowercase names (`snake_case`).
*   **Missing Order IDs:** Automatically deleted rows missing an `order_id` since transactions without IDs cannot be trusted.
*   **Text Inconsistency:** Fixed messy text capitalization (e.g., mixing 'rivers', 'Rivers', and 'KEYBOARD') into clean `Title Case`.
*   **Date Formats:** Converted text dates into structured date formats to allow proper time-based analysis.
*   **Missing Quantities:** Instead of deleting rows with missing numbers, empty fields in `units_sold` were filled using the data's median to keep metrics accurate.
*   **Math Errors:** Programmatically calculated the `total_sale` column using `units_sold * unit_price` to eliminate math errors from the raw data.
*   **Duplicate Records:** Found and removed double-counted duplicate entries based on unique Order IDs.

## 📁 Repository Structure
To maintain a clean professional workspace, raw files and clean outputs are kept in separate folders:

```text
├── source/
│   └── nigeria_messy_sales_dataset.csv   # Unchanged raw data
├── clean_data/
│   └── cleaned_sales_data.csv            # Cleaned final file output
├── clean_data.py                         # The data cleaning Python script
└── README.md                             # Project documentation
```

## 🚀 How to Run the Script
1. Install Pandas:
   ```bash
   pip install pandas
   ```
2. Put your raw messy dataset in the `source/` folder.
3. Run the script from your terminal:
   ```bash
   python nigeria_messy_sales_dataset.py
   ```

## Successful Code Run Screenshot

![Data Pipeline Architecture](./Successful_code_run_screenshot/Screenshot%202026-10-01%20194355.png)