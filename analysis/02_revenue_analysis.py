import pandas as pd

orders = pd.read_csv(
    "../data/orders.csv",
    parse_dates=["order_date"]
)

# Only delivered orders generate revenue
delivered = orders[orders["order_status"] == "delivered"].copy()

monthly_revenue = (
    delivered
    .groupby(delivered["order_date"].dt.to_period("M"))
    ["final_amount"]
    .sum()
    .reset_index()
)

monthly_revenue["order_date"] = monthly_revenue["order_date"].astype(str)

print("\nMonthly Revenue Trend:")
print(monthly_revenue)

# Sort by month
monthly_revenue = monthly_revenue.sort_values("order_date")

last_3 = monthly_revenue.tail(3)["final_amount"].sum()
prev_3 = monthly_revenue.tail(6).head(3)["final_amount"].sum()

print("\nRevenue Comparison:")
print(f"Last 3 months revenue     : {round(last_3, 2)}")
print(f"Previous 3 months revenue : {round(prev_3, 2)}")

growth_pct = ((last_3 - prev_3) / prev_3) * 100 if prev_3 != 0 else 0
print(f"Growth %                  : {round(growth_pct, 2)}%")

monthly_revenue.to_csv("../data/monthly_revenue_summary.csv", index=False)