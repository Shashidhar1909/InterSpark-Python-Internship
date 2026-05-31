import logging
from pathlib import Path
from typing import Optional

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"
LOGS_DIR = BASE_DIR / "logs"
DEFAULT_CSV = DATA_DIR / "sales_data.csv"
REPORT_FILE = OUTPUTS_DIR / "analysis_report.txt"

LOGS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=str(LOGS_DIR / "operations.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def money(value: float) -> str:
    return f"${value:,.2f}"


def load_data(path: Path) -> pd.DataFrame:
    logging.info("Loading data from %s", path)
    df = pd.read_csv(path)
    required = {"OrderID", "OrderDate", "Region", "Category", "Product", "Quantity", "UnitPrice", "Discount"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Cleaning data")
    df = df.copy()

    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
    numeric_cols = ["Quantity", "UnitPrice", "Discount"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.drop_duplicates(subset=["OrderID"])
    df = df.dropna(subset=["OrderID", "OrderDate", "Region", "Category", "Product", "Quantity", "UnitPrice"])
    df["Discount"] = df["Discount"].fillna(0)

    df["NetSales"] = df["Quantity"] * df["UnitPrice"] * (1 - df["Discount"])
    df["Month"] = df["OrderDate"].dt.strftime("%Y-%m")
    df["DayName"] = df["OrderDate"].dt.day_name()

    logging.info("Rows after cleaning: %s", len(df))
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    print("\nAvailable filters:")
    print("1. No filter")
    print("2. Filter by region")
    print("3. Filter by category")
    print("4. Filter by minimum net sales per order")
    choice = input("Enter filter choice (1/2/3/4): ").strip()

    filtered = df.copy()

    if choice == "2":
        region = input("Enter region (North/South/East/West): ").strip().title()
        filtered = filtered[filtered["Region"].str.title() == region]
        logging.info("Filtered by region: %s", region)
    elif choice == "3":
        category = input("Enter category (Electronics/Books/Clothing/Home): ").strip().title()
        filtered = filtered[filtered["Category"].str.title() == category]
        logging.info("Filtered by category: %s", category)
    elif choice == "4":
        threshold = float(input("Enter minimum net sales: ").strip())
        filtered = filtered[filtered["NetSales"] >= threshold]
        logging.info("Filtered by minimum net sales >= %s", threshold)
    else:
        logging.info("No filter applied")

    return filtered


def build_summary(df: pd.DataFrame) -> str:
    total_orders = df["OrderID"].nunique()
    total_quantity = int(df["Quantity"].sum())
    total_sales = df["NetSales"].sum()
    average_order_value = df["NetSales"].mean() if len(df) else 0

    region_summary = (
        df.groupby("Region", as_index=False)["NetSales"]
        .sum()
        .sort_values("NetSales", ascending=False)
    )
    category_summary = (
        df.groupby("Category", as_index=False)["NetSales"]
        .sum()
        .sort_values("NetSales", ascending=False)
    )
    top_products = (
        df.groupby("Product", as_index=False)["NetSales"]
        .sum()
        .sort_values("NetSales", ascending=False)
        .head(5)
    )

    lines = []
    lines.append("Python Data Analysis Project")
    lines.append("=" * 32)
    lines.append(f"Rows after cleaning : {len(df)}")
    lines.append(f"Unique orders       : {total_orders}")
    lines.append(f"Total quantity sold : {total_quantity}")
    lines.append(f"Total revenue       : {money(total_sales)}")
    lines.append(f"Average order value : {money(average_order_value)}")
    lines.append("")
    lines.append("Revenue by region:")
    for _, row in region_summary.iterrows():
        lines.append(f"  - {row['Region']}: {money(row['NetSales'])}")
    lines.append("")
    lines.append("Revenue by category:")
    for _, row in category_summary.iterrows():
        lines.append(f"  - {row['Category']}: {money(row['NetSales'])}")
    lines.append("")
    lines.append("Top 5 products by revenue:")
    for _, row in top_products.iterrows():
        lines.append(f"  - {row['Product']}: {money(row['NetSales'])}")
    lines.append("")
    lines.append("Insights:")
    lines.append("  - Cleaned the dataset by removing duplicates and invalid rows.")
    lines.append("  - Calculated net sales after discount.")
    lines.append("  - Grouped data by region, category, and product for analysis.")

    return "\n".join(lines)


def save_report(report: str) -> None:
    REPORT_FILE.write_text(report, encoding="utf-8")
    logging.info("Saved analysis report to %s", REPORT_FILE)


def main() -> None:
    print("Python Data Analysis Project")
    print("=" * 30)

    try:
        use_default = input(f"Use sample dataset at {DEFAULT_CSV}? (y/n): ").strip().lower()
        if use_default in ("", "y", "yes"):
            csv_path = DEFAULT_CSV
        else:
            csv_input = input("Enter CSV file path: ").strip()
            csv_path = Path(csv_input)

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        df = load_data(csv_path)
        print(f"Loaded {len(df)} rows from {csv_path.name}")

        cleaned = clean_data(df)
        print(f"Rows after cleaning: {len(cleaned)}")

        filtered = apply_filters(cleaned)
        print(f"Rows after filter: {len(filtered)}")

        report = build_summary(filtered)
        save_report(report)

        print("\n" + report)
        print(f"\nReport saved to: {REPORT_FILE}")
        print("Task completed successfully.")
        logging.info("Task completed successfully")

    except Exception as exc:
        logging.exception("Error while running data analysis project")
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
