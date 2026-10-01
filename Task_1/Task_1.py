import os
import pandas as pd

# Define raw data file paths
RAW_DATA_PATH = os.path.join("source", "Online_Sales_Data.csv")

# Output file paths
CLEANED_DIR_PATH = "cleaned_data"
CLEANED_DATA_PATH = os.path.join(
    CLEANED_DIR_PATH, "cleaned_online_sales_data.csv"
)


def clean_transaction_data():
    print("🚀 Starting Data Cleaning Pipeline...")

    # 1. Load Dataset Safely
    if not os.path.exists(RAW_DATA_PATH):
        print(f"❌ Error: Could not find '{RAW_DATA_PATH}'. Please check the filename.")
        return
    df = pd.read_csv(RAW_DATA_PATH)

    # 2. Standardize Column Names (Lowercase, no spaces)
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    )

    # 3. Handle Missing Values (Nulls)
    df = df.dropna(subset=["transaction_id"])
    df["units_sold"] = df["units_sold"].fillna(0)
    df["unit_price"] = df["unit_price"].fillna(0.0)

    # 4. Correct Data Types (With errors='coerce' to prevent sudden terminal crashes)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = df["units_sold"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)

    # 5. Remove Duplicate Records
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")

    # 6. Standardize Text Strings
    string_columns = [
        "product_category",
        "product_name",
        "region",
        "payment_method",
    ]
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    # 7. Recalculate Total Revenue
    df["total_revenue"] = (df["units_sold"] * df["unit_price"]).round(2)

    # 8. Create output file directory
    if not os.path.exists(CLEANED_DIR_PATH):
        os.makedirs(CLEANED_DIR_PATH)
        print(f"📁 Created missing directory: '{CLEANED_DIR_PATH}/'")

    # 9. Export Cleaned Dataset to the new folder
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"✅ Success! Cleaned file saved to: {CLEANED_DATA_PATH}")

    # Print clean preview safely
    print(f"\n--- Cleaned Data Sample (Top 5 Rows) ---")
    print(df.head())


if __name__ == "__main__":
    clean_transaction_data()
