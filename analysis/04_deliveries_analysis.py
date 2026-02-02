import pandas as pd
import matplotlib.pyplot as plt

deliveries = pd.read_csv(
    "../data/deliveries.csv",
    parse_dates=["pickup_time", "estimated_delivery_time", "actual_delivery_time"]
)

delivered = deliveries[deliveries["delivery_status"] == "delivered"].copy()

delivered["delivery_time_minutes"] = (
    (delivered["actual_delivery_time"] - delivered["pickup_time"])
    .dt.total_seconds() / 60
).round(2)

avg_delivery_time = delivered["delivery_time_minutes"].mean()

print(f"Average delivery time: {round(avg_delivery_time, 2)} minutes")

delivered["month"] = delivered["pickup_time"].dt.to_period("M")

monthly_delivery_time = (
    delivered
    .groupby("month")["delivery_time_minutes"]
    .mean()
    .reset_index()
)

monthly_delivery_time["delivery_time_minutes"] = monthly_delivery_time["delivery_time_minutes"].round(2)

monthly_delivery_time["month"] = monthly_delivery_time["month"].astype(str)

print("\nMonthly Avg Delivery Time:")
print(monthly_delivery_time.tail(6))


delivered["is_late"] = (
    delivered["actual_delivery_time"] > delivered["estimated_delivery_time"]
)

late_rate = delivered["is_late"].mean() * 100

print(f"\nLate delivery rate: {round(late_rate, 2)}%")

agent_performance = (
    delivered
    .groupby("delivery_agent_id")
    .agg(
        total_deliveries=("delivery_id", "count"),
        avg_delivery_time=("delivery_time_minutes", "mean"),
        late_rate_pct=("is_late", "mean")
    )
    .reset_index()
)

agent_performance["late_rate_pct"] *= 100

print("\nTop 5 Slowest Agents:")
print(
    agent_performance
    .sort_values("avg_delivery_time", ascending=False)
    .head(5)
)

plt.figure(figsize=(8, 4))
plt.plot(
    monthly_delivery_time["month"],
    monthly_delivery_time["delivery_time_minutes"],
    marker="o"
)

plt.title("Monthly Average Delivery Time")
plt.xlabel("Month")
plt.ylabel("Minutes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()