import os
import pandas as pd

# Define clean path structures
RAW_DATA_PATH = os.path.join("source", "nigeria_messy_sales_dataset.csv")
CLEANED_DIR_PATH = os.path.join("clean_data")
CLEANED_DATA_PATH = os.path.join(CLEANED_DIR_PATH, "cleaned_sales_data.csv")

def run_data_cleaning_pipeline():
    print("=" * 50)
    print("📋 STARTING DATA ANALYST INGESTION & CLEANING PIPELINE\n")
    print("=" * 50)
    
    # --- STEP 1: SAFE FILE INGESTION ---
    if not os.path.exists(RAW_DATA_PATH):
        print(f"❌ CRITICAL ERROR: Could not locate raw source dataset at: {RAW_DATA_PATH}")
        return
        
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"📊 Successfully loaded dataset. Shape: {df.shape[0]} rows, {df.shape[1]} columns.\n")
    
    # --- STEP 2: COLUMN HEADER STANDARDIZATION ---
    # Standardizing to lower_snake_case prevents typos during future analysis
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_', regex=False)
    print("✅ Normalized all column headers to standard snake_case format.\n")
    
    # --- STEP 3: DATA INTEGRITY AUDIT (MISSING ORDER IDs) ---
    # In a business environment, a transaction without an Order ID or identifier cannot be trusted
    initial_count = len(df)
    df = df.dropna(subset=['order_id'])
    pruned_count = initial_count - len(df)
    if pruned_count > 0:
        print(f"🗑️ Safely dropped {pruned_count} corrupted records missing critical 'order_id' values.\n")
    
    # --- STEP 4: TEXT CATEGORY STANDARDIZATION ---
    # Fixes variations like 'KEYBOARD' vs 'Keyboard' and lowercase state records
    categorical_columns = ['customer_name', 'state', 'product', 'sales_channel']
    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    print("📝 Standardized all categorical text columns to uniform Title Case.\n")
    
    # --- STEP 5: DATE TYPE CASTING ---
    # Enforces standard date parsing
    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
    print("📅 Converted text transaction timelines into structured Datetime formats.\n")
    
    # --- STEP 6: SMART IMPUTATION FOR QUANTITIES ---
    # Dropping rows missing quantities loses valuable data. Imputing with the median preserves it!
    if 'units_sold' in df.columns:
        units_median = df['units_sold'].median()
        # Safe fallback if median calculation evaluates to null or zero
        if pd.isna(units_median) or units_median == 0:
            units_median = 1
            
        df['units_sold'] = df['units_sold'].fillna(units_median).astype(int)
        print(f"🔢 Imputed missing quantities in 'units_sold' using the data median ({int(units_median)}).\n")
    
    if 'unit_price' in df.columns:
        df['unit_price'] = df['unit_price'].fillna(0.0).astype(float)
        
    # --- STEP 7: COMPUTATIONAL FINANCIAL RECALCULATION ---
    # Recalculating totals programmatically eliminates baseline arithmetic errors in the raw entries
    if 'units_sold' in df.columns and 'unit_price' in df.columns:
        df['total_sale'] = (df['units_sold'] * df['unit_price']).round(2)
        print("💰 Calculated 'total_sale' metrics algorithmically to guarantee 100% financial accuracy.\n")
        
    # --- STEP 8: STRICT DE-DUPLICATION ---
    # Ensures every record left in our workspace represents a completely unique transaction
    pre_dedup_count = len(df)
    df = df.drop_duplicates(subset=['order_id'], keep='first')
    dedup_removed = pre_dedup_count - len(df)
    print(f"✨ Successfully dropped {dedup_removed} duplicate row records based on strict Order IDs.\n")
    
    # --- STEP 9: Create Output File Directory ---
    if not os.path.exists(CLEANED_DIR_PATH):
        os.makedirs(CLEANED_DIR_PATH)
        print(f"📁 Initialized directory path: {CLEANED_DIR_PATH}/")
        
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print("=" * 50)
    print(f"🎉 SCRIPT RUN SUCCESSFUL! Cleaned dataset stored at: {CLEANED_DATA_PATH}\n")
    print(f"📊 Final Clean Record Count: {len(df)} rows.")
    print("=" * 50)

if __name__ == "__main__":
    run_data_cleaning_pipeline()
