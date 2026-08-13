import pandas as pd

source_a = pd.read_csv("source_a.csv")
source_b = pd.read_csv("source_b.csv")

# Calculate Sales
source_a["Sales"] = source_a["Quantity"] * source_a["Price"]

source_b["Sales"] = (
    source_b["Quantity"] * source_b["Price"]
    - source_b["Discount"]
)
# Calculate total sales
sales_a = source_a["Sales"].sum()
sales_b = source_b["Sales"].sum()

# Calculate difference
difference = abs(sales_a - sales_b)

print("\n========== METRIC ANALYSIS ==========")

print("Source A Sales:", sales_a)
print("Source B Sales:", sales_b)
print("Difference:", difference)

# Find orders missing from Source B
orders_a = set(source_a["Order_ID"])
orders_b = set(source_b["Order_ID"])

missing_in_b = orders_a - orders_b
missing_in_a = orders_b - orders_a

print("\n========== REASON ANALYSIS ==========")

if missing_in_b:

    print("⚠️ Source B is missing orders from Source A.")

    for order_id in missing_in_b:

        order = source_a[source_a["Order_ID"] == order_id].iloc[0]

        print(
            "Order:", order_id,
            "| Status:", order["Status"],
            "| Sales:", order["Sales"]
        )

        if order["Status"] == "Cancelled":
            print("→ This order is CANCELLED.")
            print("→ Possible root cause: Different handling of cancelled orders.")

if missing_in_a:
    print("⚠️ Source A is missing orders from Source B.")

# Check duplicate orders
duplicates_a = source_a[source_a.duplicated("Order_ID", keep=False)]
duplicates_b = source_b[source_b.duplicated("Order_ID", keep=False)]

if not duplicates_a.empty:

    print("\n⚠️ Duplicate orders found in Source A:")
    print(duplicates_a[["Order_ID", "Sales"]])

if not duplicates_b.empty:

    print("\n⚠️ Duplicate orders found in Source B:")
    print(duplicates_b[["Order_ID", "Sales"]])

print("\n========== FINAL RESULT ==========")

if difference == 0:
    print("✅ No mismatch detected.")

else:
    print("⚠️ MISMATCH DETECTED")
    print("Difference:", difference)

    if missing_in_b:
        print("🔎 Root Cause: Source A and Source B handle some orders differently.")

    if not duplicates_a.empty or not duplicates_b.empty:
        print("🔎 Additional Issue: Duplicate records detected.")
        # Check date ranges

source_a["Date"] = pd.to_datetime(source_a["Date"])
source_b["Date"] = pd.to_datetime(source_b["Date"])

min_date_a = source_a["Date"].min()
max_date_a = source_a["Date"].max()

min_date_b = source_b["Date"].min()
max_date_b = source_b["Date"].max()

print("\n========== DATE CHECK ==========")

print("Source A:", min_date_a.date(), "to", max_date_a.date())
print("Source B:", min_date_b.date(), "to", max_date_b.date())

if min_date_a != min_date_b or max_date_a != max_date_b:
    print("⚠️ Date range mismatch detected.")
    print("→ Possible reason: Different date ranges are being used.")
else:
    print("✅ Date ranges are the same.")
    print("\n========== FORMULA CHECK ==========")

print("Source A formula: Quantity × Price")
print("Source B formula: Quantity × Price − Discount")

if "Discount" in source_b.columns:
    print("⚠️ Formula logic is different.")
    print("→ Source B subtracts Discount.")
    print("→ This can cause a metric mismatch.")
else:
    print("⚠️ Discount column not found in Source B.")
    print("\n========== ROOT CAUSE ENGINE ==========")

reasons = []

# Check missing records
if missing_in_a or missing_in_b:
    reasons.append("Missing records")

# Check duplicates
if not duplicates_a.empty or not duplicates_b.empty:
    reasons.append("Duplicate records")

# Check date range
if min_date_a != min_date_b or max_date_a != max_date_b:
    reasons.append("Different date ranges")

# Formula difference
if "Discount" in source_b.columns:
    reasons.append("Different calculation formula")

print("Issues detected:")

for reason in reasons:
    print("→", reason)

if len(reasons) == 1:
    print("\n🔎 MAIN ROOT CAUSE:", reasons[0])

elif len(reasons) > 1:
    print("\n⚠️ MULTIPLE POSSIBLE ROOT CAUSES")
    print("→ Human review is recommended.")

else:
    print("\n✅ No root cause detected.")
    print("\n========== EVIDENCE SCORE ==========")

scores = {}

if missing_in_a or missing_in_b:
    scores["Missing records"] = 90

if not duplicates_a.empty or not duplicates_b.empty:
    scores["Duplicate records"] = 95

if min_date_a != min_date_b or max_date_a != max_date_b:
    scores["Different date ranges"] = 90

if "Discount" in source_b.columns:
    scores["Different calculation formula"] = 85

for reason, score in scores.items():
    print(f"{reason}: {score}% evidence")

if scores:
    strongest_reason = max(scores, key=scores.get)
    strongest_score = scores[strongest_reason]

    print("\n🔎 Strongest evidence:")
    print(strongest_reason)
    print("Evidence:", strongest_score, "%")
else:
    print("No evidence found.")
    print("\n========== FINAL RECOMMENDATION ==========")

if difference == 0:
    print("🟢 SAFE")
    print("Both sources have the same value.")

elif len(reasons) == 1:
    print("🟢 RECOMMENDATION")
    print("One main issue was detected.")
    print("Review:", reasons[0])

else:
    print("🟡 HUMAN REVIEW REQUIRED")
    print("Multiple issues were detected.")
    print("Do not automatically select one value.")
    print("\n========== FINAL REPORT ==========")

print("Metric: Sales")
print("Source A:", sales_a)
print("Source B:", sales_b)
print("Difference:", difference)

print("\nIssues found:")

if reasons:
    for reason in reasons:
        print("•", reason)
else:
    print("• No issues found")

print("\nRecommendation:")

if difference == 0:
    print("🟢 Values match. No action required.")

elif len(reasons) == 1:
    print("🟢 Review the detected issue:", reasons[0])

else:
    print("🟡 Human review required.")
    print("Multiple factors may be causing the mismatch.")

print("\n===================================")