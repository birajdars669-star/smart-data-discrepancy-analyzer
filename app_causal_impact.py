import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Causal Impact Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Smart Causal Impact Analyzer")

st.write(
    "Compare two data sources and identify order-level differences."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    file_a = st.file_uploader(
        "Upload Source A",
        type=["csv"],
        key="causal_a"
    )

with col2:
    file_b = st.file_uploader(
        "Upload Source B",
        type=["csv"],
        key="causal_b"
    )

if file_a and file_b:

    source_a = pd.read_csv(file_a)
    source_b = pd.read_csv(file_b)

    st.success("Both files uploaded successfully!")

    required = [
        "Order_ID",
        "Date",
        "Product",
        "Quantity",
        "Price",
        "Status"
    ]

    missing_a = [c for c in required if c not in source_a.columns]
    missing_b = [c for c in required if c not in source_b.columns]

    if missing_a or missing_b:

        st.error("Required columns are missing.")

        if missing_a:
            st.write("Source A missing:", missing_a)

        if missing_b:
            st.write("Source B missing:", missing_b)

    else:

        # Sales calculation
        source_a["Sales"] = (
            source_a["Quantity"] * source_a["Price"]
        )

        if "Discount" in source_b.columns:
            source_b["Sales"] = (
                source_b["Quantity"] * source_b["Price"]
                - source_b["Discount"]
            )
        else:
            source_b["Sales"] = (
                source_b["Quantity"] * source_b["Price"]
            )

        # Order IDs
        orders_a = set(source_a["Order_ID"])
        orders_b = set(source_b["Order_ID"])

        common_orders = orders_a & orders_b
        missing_in_b = orders_a - orders_b
        missing_in_a = orders_b - orders_a

        # Order-level comparison
        results = []

        for order_id in common_orders:

            row_a = source_a[
                source_a["Order_ID"] == order_id
            ].iloc[0]

            row_b = source_b[
                source_b["Order_ID"] == order_id
            ].iloc[0]

            quantity_diff = (
                row_a["Quantity"] != row_b["Quantity"]
            )

            price_diff = (
                row_a["Price"] != row_b["Price"]
            )

            sales_a = float(row_a["Sales"])
            sales_b = float(row_b["Sales"])

            sales_impact = abs(sales_a - sales_b)

            if quantity_diff:
                cause = "Quantity mismatch"

            elif price_diff:
                cause = "Price mismatch"

            elif sales_impact != 0:
                cause = "Sales calculation mismatch"

            else:
                cause = "No difference"

            if cause != "No difference":

                results.append({
                    "Order_ID": order_id,
                    "Cause": cause,
                    "Impact": sales_impact
                })

        # Issues
        st.subheader("⚠️ Issues Detected")

        issues = []

        if missing_in_a or missing_in_b:
            issues.append("Missing records")

        duplicates_a = source_a[
            source_a.duplicated("Order_ID", keep=False)
        ]

        duplicates_b = source_b[
            source_b.duplicated("Order_ID", keep=False)
        ]

        if not duplicates_a.empty or not duplicates_b.empty:
            issues.append("Duplicate records")

        if results:
            issues.append("Order-level metric differences")

        if issues:
            for issue in issues:
                st.write("•", issue)
        else:
            st.success("No issues detected.")

        # Smart Root Cause Analyzer
        st.divider()

        st.subheader("🧠 Smart Root Cause Analyzer")

        if results:

            result_df = pd.DataFrame(results)

            st.dataframe(
                result_df,
                use_container_width=True
            )

            strongest = result_df.iloc[0]

            st.warning(
                f"🔴 Main Root Cause: "
                f"{strongest['Cause']} "
                f"in Order {strongest['Order_ID']}"
            )

            total_impact = result_df["Impact"].sum()

            st.write(
                f"Estimated impact: ₹{total_impact:,.0f}"
            )

        else:
            st.success("No root cause detected.")

        # Order level details
        st.divider()

        st.subheader("📋 Order-Level Difference Analysis")

        details = []

        for order_id in common_orders:

            row_a = source_a[
                source_a["Order_ID"] == order_id
            ].iloc[0]

            row_b = source_b[
                source_b["Order_ID"] == order_id
            ].iloc[0]

            details.append({
                "Order_ID": order_id,
                "A_Quantity": row_a["Quantity"],
                "B_Quantity": row_b["Quantity"],
                "A_Price": row_a["Price"],
                "B_Price": row_b["Price"],
                "A_Sales": row_a["Sales"],
                "B_Sales": row_b["Sales"],
                "Sales_Impact": abs(
                    row_a["Sales"] - row_b["Sales"]
                )
            })

        if details:

            detail_df = pd.DataFrame(details)

            st.dataframe(
                detail_df,
                use_container_width=True
            )

        # Date range
        st.divider()

        st.subheader("📅 Date Range Check")

        source_a["Date"] = pd.to_datetime(source_a["Date"])
        source_b["Date"] = pd.to_datetime(source_b["Date"])

        min_a = source_a["Date"].min()
        max_a = source_a["Date"].max()

        min_b = source_b["Date"].min()
        max_b = source_b["Date"].max()

        d1, d2 = st.columns(2)

        d1.write(
            f"**Source A:** {min_a.date()} → {max_a.date()}"
        )

        d2.write(
            f"**Source B:** {min_b.date()} → {max_b.date()}"
        )

        if min_a == min_b and max_a == max_b:
            st.success("Date ranges are the same.")
        else:
            st.warning("Date range mismatch detected.")

else:

    st.info(
        "Upload Source A and Source B CSV files to start analysis."
    )