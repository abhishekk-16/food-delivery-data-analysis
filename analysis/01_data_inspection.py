import pandas as pd

orders = pd.read_csv(
    "../data/orders.csv",
    parse_dates=["order_date", "created_at", "updated_at"]
)

print("Shape:", orders.shape)
print("\nColumns:")
print(orders.columns)

print("\nData types:")
print(orders.dtypes)

print("\nMissing values:")
print(orders.isna().sum())

print("\nSample data:")
print(orders.head())

print("\nOrder status distribution:")
print(orders["order_status"].value_counts())

print("\nMissing final_amount values:")
print(orders["final_amount"].isna().sum())