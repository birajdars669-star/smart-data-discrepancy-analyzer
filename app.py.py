import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Metric Checker",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Smart Metric Checker")
st.write(
    "Compare two data sources, detect metric mismatches, "
    "and identify the likely root cause."
)

st.divider()

# -----------------------------
# UPLOAD FILES
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    file_a = st.file_uploader(
        "Upload Source A",
        type=["csv"],
        key="source_a"
    )

with col2:
    file_b = st.file_uploader(
        "Upload Source B",
        type=["csv"],
        key="source_b"
    )

if file_a and file_b:

    source_a = pd.read_csv(file_a)
    source_b = pd.read_csv(file_b)

    st.success("Both files uploaded successfully!")

    # -----------------------------
    # REQUIRED COLUMNS
    # -----------------------------

    required_columns = [
        "Order_ID",
        "Date",
        "Quantity",
        "Price",
        "Status"
    ]

    missing_a = [
        col for col in required_columns
        if col not in source_a.columns
    ]

    missing_b = [
        col for col in required_columns
        if col not in source_b.columns
    ]

    if missing_a or missing_b:

        st.error("Required columns are missing.")

        if missing_a:
            st.write("Source A missing:", missing_a)

        if missing_b:
            st.write("Source B missing:", missing_b)

    else:

        # -----------------------------
        # CLEAN DATA
        # -----------------------------

        source_a["Date"] = pd.to_datetime(
            source_a["Date"],
            errors="coerce"
        )

        source_b["Date"] = pd.to_datetime(
            source_b["Date"],
            errors="coerce"
        )

        source_a["Quantity"] = pd.to_numeric(
            source_a["Quantity"],
            errors="coerce"
        )

        source_b["Quantity"] = pd.to_numeric(
            source_b["Quantity"],
            errors="coerce"
        )

        source_a["Price"] = pd.to_numeric(
            source_a["Price"],
            errors="coerce"
        )

        source_b["Price"] = pd.to_numeric(
            source_b["Price"],
            errors="coerce"
        )

        # -----------------------------
        # CALCULATE SALES
        # -----------------------------

        source_a["Sales"] = (
            source_a["Quantity"] *
            source_a["Price"]
        )

        if "Discount" in source_a.columns:
            source_a["Discount"] = pd.to_numeric(
                source_a["Discount"],
                errors="coerce"
            ).fillna(0)

            source_a["Sales"] = (
                source_a["Quantity"] *
                source_a["Price"] -
                source_a["Discount"]
            )

        if "Discount" in source_b.columns:

            source_b["Discount"] = pd.to_numeric(
                source_b["Discount"],
                errors="coerce"
            ).fillna(0)

            source_b["Sales"] = (
                source_b["Quantity"] *
                source_b["Price"] -
                source_b["Discount"]
            )

        else:

            source_b["Sales"] = (
                source_b["Quantity"] *
                source_b["Price"]
            )

        # -----------------------------
        # TOTAL SALES
        # -----------------------------

        sales_a = source_a["Sales"].sum()
        sales_b = source_b["Sales"].sum()

        difference = abs(sales_a - sales_b)

        # -----------------------------
        # ORDER IDS
        # -----------------------------

        orders_a = set(source_a["Order_ID"])
        orders_b = set(source_b["Order_ID"])

        missing_in_b = orders_a - orders_b
        missing_in_a = orders_b - orders_a

        # -----------------------------
        # DUPLICATES
        # -----------------------------

        duplicates_a = source_a[
            source_a.duplicated(
                "Order_ID",
                keep=False
            )
        ]

        duplicates_b = source_b[
            source_b.duplicated(
                "Order_ID",
                keep=False
            )
        ]

        # -----------------------------
        # DATE RANGE
        # -----------------------------

        min_date_a = source_a["Date"].min()
        max_date_a = source_a["Date"].max()

        min_date_b = source_b["Date"].min()
        max_date_b = source_b["Date"].max()

        date_mismatch = (
            min_date_a != min_date_b
            or max_date_a != max_date_b
        )

        # -----------------------------
        # ISSUES
        # -----------------------------

        reasons = []

        if missing_in_a or missing_in_b:
            reasons.append("Missing records")

        if not duplicates_a.empty or not duplicates_b.empty:
            reasons.append("Duplicate records")

        if date_mismatch:
            reasons.append("Different date ranges")

        # -----------------------------
        # ROOT CAUSE ANALYSIS
        # -----------------------------

        root_causes = []

        common_orders = orders_a.intersection(orders_b)

        comparison_rows = []

        for order_id in common_orders:

            row_a = source_a[
                source_a["Order_ID"] == order_id
            ].iloc[0]

            row_b = source_b[
                source_b["Order_ID"] == order_id
            ].iloc[0]

            quantity_diff = (
                row_a["Quantity"] -
                row_b["Quantity"]
            )

            price_diff = (
                row_a["Price"] -
                row_b["Price"]
            )

            sales_diff = (
                row_a["Sales"] -
                row_b["Sales"]
            )

            date_diff = (
                row_a["Date"] != row_b["Date"]
            )

            if (
                quantity_diff != 0
                or price_diff != 0
                or sales_diff != 0
                or date_diff
            ):

                comparison_rows.append({
                    "Order_ID": order_id,
                    "A_Quantity": row_a["Quantity"],
                    "B_Quantity": row_b["Quantity"],
                    "A_Price": row_a["Price"],
                    "B_Price": row_b["Price"],
                    "A_Sales": row_a["Sales"],
                    "B_Sales": row_b["Sales"],
                    "Sales_Impact": abs(sales_diff),
                    "Date_Mismatch": date_diff
                })

                if quantity_diff != 0:

                    root_causes.append({
                        "Order_ID": order_id,
                        "Cause": "Quantity mismatch",
                        "Impact": abs(sales_diff)
                    })

                if price_diff != 0:

                    root_causes.append({
                        "Order_ID": order_id,
                        "Cause": "Price mismatch",
                        "Impact": abs(sales_diff)
                    })

                if date_diff:

                    root_causes.append({
                        "Order_ID": order_id,
                        "Cause": "Order date mismatch",
                        "Impact": abs(sales_diff)
                    })

        # -----------------------------
        # METRIC SUMMARY
        # -----------------------------

        st.subheader("📊 Metric Summary")

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Source A Sales",
            f"₹{sales_a:,.0f}"
        )

        m2.metric(
            "Source B Sales",
            f"₹{sales_b:,.0f}"
        )

        m3.metric(
            "Difference",
            f"₹{difference:,.0f}"
        )

        st.divider()

        # -----------------------------
        # ISSUES
        # -----------------------------

        st.subheader("⚠️ Issues Detected")

        all_issues = reasons.copy()

        if root_causes:
            all_issues.append(
                "Order-level metric differences"
            )

        if all_issues:

            for issue in all_issues:
                st.write("•", issue)

        else:

            st.success(
                "No issues detected."
            )

        # -----------------------------
        # SMART ROOT CAUSE
        # -----------------------------

        st.divider()

        st.subheader(
            "🧠 Smart Root Cause Analyzer"
        )

        if root_causes:

            root_df = pd.DataFrame(
                root_causes
            )

            st.dataframe(
                root_df,
                use_container_width=True
            )

            strongest = root_df.loc[
                root_df["Impact"].idxmax()
            ]

            st.warning(
                f"🔴 Main Root Cause: "
                f"{strongest['Cause']} "
                f"in Order {strongest['Order_ID']}"
            )

            st.write(
                f"Estimated impact: "
                f"₹{strongest['Impact']:,.0f}"
            )

        elif missing_in_b or missing_in_a:

            st.info(
                "🔎 Root cause is related to "
                "missing records."
            )

        elif not duplicates_a.empty or not duplicates_b.empty:

            st.info(
                "🔎 Root cause is related to "
                "duplicate records."
            )

        elif date_mismatch:

            st.info(
                "🔎 Root cause is related to "
                "different date ranges."
            )

        else:

            st.success(
                "No root cause detected."
            )

        # -----------------------------
        # ORDER LEVEL DETAILS
        # -----------------------------

        if comparison_rows:

            st.subheader(
                "📋 Order-Level Difference Analysis"
            )

            comparison_df = pd.DataFrame(
                comparison_rows
            )

            st.dataframe(
                comparison_df,
                use_container_width=True
            )

        # -----------------------------
        # MISSING ORDERS
        # -----------------------------

        if missing_in_b:

            st.subheader(
                "🔍 Orders Missing in Source B"
            )

            missing_data = source_a[
                source_a["Order_ID"].isin(
                    missing_in_b
                )
            ]

            st.dataframe(
                missing_data,
                use_container_width=True
            )

        if missing_in_a:

            st.subheader(
                "🔍 Orders Missing in Source A"
            )

            missing_data = source_b[
                source_b["Order_ID"].isin(
                    missing_in_a
                )
            ]

            st.dataframe(
                missing_data,
                use_container_width=True
            )

        # -----------------------------
        # DUPLICATES
        # -----------------------------

        if not duplicates_a.empty:

            st.subheader(
                "🔁 Duplicate Records in Source A"
            )

            st.dataframe(
                duplicates_a,
                use_container_width=True
            )

        if not duplicates_b.empty:

            st.subheader(
                "🔁 Duplicate Records in Source B"
            )

            st.dataframe(
                duplicates_b,
                use_container_width=True
            )

        # -----------------------------
        # DATE CHECK
        # -----------------------------

        st.subheader(
            "📅 Date Range Check"
        )

        d1, d2 = st.columns(2)

        d1.write(
            f"**Source A:** "
            f"{min_date_a.date()} → "
            f"{max_date_a.date()}"
        )

        d2.write(
            f"**Source B:** "
            f"{min_date_b.date()} → "
            f"{max_date_b.date()}"
        )

        if date_mismatch:

            st.warning(
                "Date range mismatch detected."
            )

        else:

            st.success(
                "Date ranges are the same."
            )

        # -----------------------------
        # FORMULA CHECK
        # -----------------------------

        st.subheader(
            "🧮 Formula Check"
        )

        st.write(
            "Source A: Quantity × Price"
        )

        if "Discount" in source_a.columns:

            st.write(
                "Source A includes Discount."
            )

        if "Discount" in source_b.columns:

            st.write(
                "Source B: Quantity × Price − Discount"
            )

            if "Discount" not in source_a.columns:

                st.warning(
                    "Calculation logic differs "
                    "because Source B uses Discount."
                )

            else:

                st.success(
                    "Both sources include Discount logic."
                )

        else:

            st.write(
                "Source B: Quantity × Price"
            )

            if "Discount" not in source_a.columns:

                st.success(
                    "Same calculation logic detected."
                )

        # -----------------------------
        # FINAL RECOMMENDATION
        # -----------------------------

        st.divider()

        st.subheader(
            "🎯 Final Recommendation"
        )

        if difference == 0 and not all_issues:

            st.success(
                "🟢 SAFE — Values match and "
                "no issues were detected."
            )

        elif root_causes:

            strongest = root_df.loc[
                root_df["Impact"].idxmax()
            ]

            st.error(
                f"🔴 ACTION REQUIRED — "
                f"Check {strongest['Cause']} "
                f"for Order {strongest['Order_ID']}."
            )

            st.write(
                f"Estimated metric impact: "
                f"₹{strongest['Impact']:,.0f}"
            )

        elif len(all_issues) == 1:

            st.warning(
                f"🟡 REVIEW REQUIRED — "
                f"{all_issues[0]}"
            )

        else:

            st.warning(
                "🟡 HUMAN REVIEW REQUIRED"
            )

            st.write(
                "Multiple factors may be causing "
                "the metric mismatch."
            )

else:

    st.info(
        "Upload Source A and Source B CSV files "
        "to start analysis."
    )