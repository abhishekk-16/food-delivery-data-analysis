import pandas as pd
import matplotlib.pyplot as plt

orders = pd.read_csv(
    "../data/orders.csv",
    parse_dates=["order_date"]
)

total_orders = len(orders)
cancelled_orders = (orders["order_status"] == "cancelled").sum()

cancellation_rate = round(
    (cancelled_orders / total_orders) * 100, 2
)

print(f"Overall cancellation rate: {cancellation_rate}%")

orders["month"] = orders["order_date"].dt.to_period("M")

monthly_cancellations = (
    orders
    .assign(is_cancelled = orders["order_status"] == "cancelled")
    .groupby("month")
    .agg(
        total_orders=("order_status", "count"),
        cancelled_orders=("is_cancelled", "sum")
    )
    .reset_index()
)

monthly_cancellations["cancellation_rate_pct"] = (
    monthly_cancellations["cancelled_orders"]
    / monthly_cancellations["total_orders"]
    * 100
).round(2)

monthly_cancellations["month"] = monthly_cancellations["month"].astype(str)

print("\nMonthly Cancellation Trend:")
print(monthly_cancellations.tail(6))

monthly_cancellations = monthly_cancellations.sort_values("month")

last_3 = monthly_cancellations.tail(3)["cancellation_rate_pct"].mean()
prev_3 = monthly_cancellations.tail(6).head(3)["cancellation_rate_pct"].mean()

print("\nCancellation Trend Comparison:")
print(f"Last 3 months avg cancellation rate     : {round(last_3, 2)}%")
print(f"Previous 3 months avg cancellation rate : {round(prev_3, 2)}%")

plt.figure(figsize=(8, 4))
plt.plot(
    monthly_cancellations["month"],
    monthly_cancellations["cancellation_rate_pct"],
    marker="o"
)

plt.title("Monthly Cancellation Rate Trend")
plt.xlabel("Month")
plt.ylabel("Cancellation Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()