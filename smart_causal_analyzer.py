import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(
    page_title="Smart Causal Impact Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# LOGO
# ============================================================
logo_path = Path("smart_causal.png")
logo_data = ""

if logo_path.exists():
    with open(logo_path, "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()

# ============================================================
# GLOBAL CSS
# ============================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 5% 20%, rgba(0, 174, 255, .13), transparent 28%),
        radial-gradient(circle at 95% 22%, rgba(184, 80, 255, .12), transparent 28%),
        linear-gradient(135deg, #020817 0%, #06152d 50%, #020817 100%);
    color: #f5f7ff;
}

.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    inset: -25%;
    pointer-events: none;
    z-index: 0;
}

.stApp::before {
    opacity: .22;
    background-image:
        radial-gradient(circle, rgba(40, 190, 255, .75) 1px, transparent 2px),
        radial-gradient(circle, rgba(194, 92, 255, .65) 1px, transparent 2px);
    background-size: 120px 120px, 170px 170px;
    animation: dataDrift 30s linear infinite;
}

.stApp::after {
    opacity: .12;
    background:
        linear-gradient(115deg, transparent 0 45%, rgba(0, 190, 255, .18) 46%, transparent 47% 100%),
        linear-gradient(65deg, transparent 0 55%, rgba(185, 80, 255, .16) 56%, transparent 57% 100%);
    background-size: 520px 520px, 640px 640px;
    animation: dataDriftReverse 38s linear infinite;
}

@keyframes dataDrift {
    from { transform: translate3d(0, 0, 0); }
    to { transform: translate3d(180px, 100px, 0); }
}

@keyframes dataDriftReverse {
    from { transform: translate3d(0, 0, 0); }
    to { transform: translate3d(-160px, -90px, 0); }
}

.block-container {
    position: relative;
    z-index: 2;
    max-width: 1500px;
    padding-top: 1.3rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071226, #020817);
    border-right: 1px solid rgba(80, 170, 255, .20);
}

.sidebar-brand {
    text-align: center;
    padding: 12px 5px 20px;
}

.sidebar-logo {
    width: 120px;
    height: 120px;
    object-fit: contain;
    border-radius: 20px;
    margin-bottom: 10px;
}

.sidebar-title {
    color: white;
    font-size: 18px;
    font-weight: 800;
    line-height: 1.25;
}

.sidebar-subtitle {
    color: #22c7ff;
    font-size: 12px;
    margin-top: 7px;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(130, 160, 200, .20);
}

[data-testid="stSidebar"] .stRadio label {
    color: #eef4ff !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] .stRadio > div {
    gap: 6px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 9px 10px;
    border-radius: 10px;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(40, 140, 255, .12);
}

/* Header */
.hero {
    text-align: center;
    padding: 8px 0 24px;
}

.main-logo {
    width: 500px;
    max-width: 80%;
    height: auto;
    display: block;
    margin: 0 auto 10px;
}

.hero h1 {
    margin: 0;
    font-size: clamp(2rem, 4vw, 3.4rem);
    font-weight: 800;
    letter-spacing: -1.5px;
    background: linear-gradient(90deg, #fff, #21c7ff, #a855f7, #fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    margin-top: 8px;
    font-weight: 700;
}

.blue { color: #22c7ff; }
.purple { color: #c084fc; }
.green { color: #34d399; }
.arrow { color: #aab5cf; padding: 0 10px; }

/* Cards */
.ui-card {
    background: linear-gradient(145deg, rgba(11, 30, 58, .94), rgba(4, 15, 33, .88));
    border: 1px solid rgba(90, 175, 255, .28);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 14px 42px rgba(0,0,0,.28), inset 0 0 25px rgba(20,100,180,.05);
}

.upload-card {
    min-height: 150px;
}

.upload-card h3 {
    margin: 0 0 5px;
    color: #22c7ff;
}

.upload-card p {
    margin: 0 0 14px;
    color: #b7c3da;
}

.ready-card {
    text-align: center;
    min-height: 150px;
}

.ready-icon {
    font-size: 42px;
    filter: drop-shadow(0 0 15px rgba(70, 180, 255, .55));
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(4, 18, 39, .62);
    border: 1px dashed rgba(70, 180, 255, .55);
    border-radius: 14px;
    padding: 8px;
}

/* Buttons */
div.stButton > button {
    width: 100%;
    min-height: 52px;
    border: 0;
    border-radius: 14px;
    color: white;
    font-size: 1.05rem;
    font-weight: 800;
    background: linear-gradient(90deg, #1598ff, #7c3aed);
    box-shadow: 0 0 30px rgba(70, 120, 255, .28);
    transition: .2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 42px rgba(115, 80, 255, .42);
}

/* KPI */
.kpi {
    min-height: 125px;
    padding: 17px;
    border-radius: 16px;
    background: linear-gradient(145deg, rgba(10, 29, 57, .95), rgba(5, 16, 34, .9));
    border: 1px solid rgba(90, 170, 255, .24);
    box-shadow: 0 10px 32px rgba(0,0,0,.24);
}

.kpi-label {
    color: #aab7cc;
    font-size: .78rem;
    font-weight: 600;
}

.kpi-value {
    color: #fff;
    font-size: 1.55rem;
    font-weight: 800;
    margin: 6px 0;
}

.kpi-sub {
    color: #34d399;
    font-size: .74rem;
}

/* Process */
.process {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 22px 0;
    padding: 19px;
    border-radius: 18px;
    background: rgba(8, 24, 48, .88);
    border: 1px solid rgba(80, 170, 255, .25);
}

.process-item {
    flex: 1;
    text-align: center;
}

.process-icon {
    font-size: 31px;
}

.process-title {
    margin-top: 5px;
    font-weight: 800;
}

.process-desc {
    color: #9eabc1;
    font-size: .78rem;
}

.process-arrow {
    color: #65c9ff;
    font-size: 30px;
}

/* Section */
.section-title {
    margin: 25px 0 12px;
    color: #22c7ff;
    font-size: 1.1rem;
    font-weight: 800;
}

/* Streamlit chrome */
#MainMenu, footer {
    visibility: hidden;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Responsive */
@media (max-width: 900px) {
    .process {
        flex-direction: column;
    }

    .process-arrow {
        transform: rotate(90deg);
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    if logo_data:
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <img src="data:image/png;base64,{logo_data}" class="sidebar-logo">
                <div class="sidebar-title">Smart Causal<br>Impact Analyzer</div>
                <div class="sidebar-subtitle">Intelligent Data Comparison</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-title">🧠 Smart Causal<br>Impact Analyzer</div>
                <div class="sidebar-subtitle">Intelligent Data Comparison</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    menu = st.radio(
        "MENU",
        [
            "🏠  Home",
            "🔍  Analyze",
            "🕘  History",
            "ℹ️  About",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=True,
        key="dark_mode",
    )

# ============================================================
# HEADER
# ============================================================
if logo_data:
    st.markdown(
        f"""
        <div class="hero">
            <img src="data:image/png;base64,{logo_data}" class="main-logo">
            <h1>Smart Causal Impact Analyzer</h1>
            <div class="hero-sub">
                <span class="blue">Metric Mismatch</span>
                <span class="arrow">→</span>
                <span class="purple">Root Cause</span>
                <span class="arrow">→</span>
                <span class="green">Financial Impact</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="hero">
            <h1>Smart Causal Impact Analyzer</h1>
            <div class="hero-sub">
                <span class="blue">Metric Mismatch</span>
                <span class="arrow">→</span>
                <span class="purple">Root Cause</span>
                <span class="arrow">→</span>
                <span class="green">Financial Impact</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# SIDEBAR PAGE CONTENT
# ============================================================
if menu.startswith("🕘"):
    st.markdown(
        '<div class="section-title">🕘 HISTORY</div>',
        unsafe_allow_html=True,
    )
    st.info("Analysis history will appear here after saved analysis sessions are added.")
    st.stop()

if menu.startswith("ℹ️"):
    st.markdown(
        '<div class="section-title">ℹ️ ABOUT</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="ui-card">
            <h2>Smart Causal Impact Analyzer</h2>
            <p>
                A data analytics tool that compares two data sources,
                detects metric mismatches, identifies possible root causes,
                and estimates financial impact.
            </p>
            <p><b>Workflow:</b> Compare → Detect → Analyze → Explain → Impact</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ============================================================
# UPLOAD FILES
# ============================================================
st.markdown(
    '<div class="section-title">📂 DATA SOURCES</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 1, 0.9], gap="large")

with col1:
    st.markdown(
        """
        <div class="ui-card upload-card">
            <h3>📁 SOURCE A</h3>
            <p>Upload first data source (CSV)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    file_a = st.file_uploader(
        "Upload Source A",
        type=["csv"],
        key="source_a",
        label_visibility="collapsed",
    )

with col2:
    st.markdown(
        """
        <div class="ui-card upload-card">
            <h3 style="color:#c084fc;">📁 SOURCE B</h3>
            <p>Upload second data source (CSV)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    file_b = st.file_uploader(
        "Upload Source B",
        type=["csv"],
        key="source_b",
        label_visibility="collapsed",
    )

with col3:
    st.markdown(
        """
        <div class="ui-card ready-card">
            <div class="ready-icon">🔎</div>
            <h3>Ready to Analyze</h3>
            <p>Compare data, detect mismatches, find root causes and calculate impact.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    analyze = st.button("⚡ Analyze Data", use_container_width=True)

# ============================================================
# START MESSAGE
# ============================================================
if not file_a or not file_b:
    st.markdown(
        """
        <div class="ui-card" style="text-align:center;margin-top:22px;">
            <h3>🚀 Start Your Analysis</h3>
            <p>Upload Source A and Source B CSV files, then click <b>Analyze Data</b>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ============================================================
# READ DATA
# ============================================================
try:
    source_a = pd.read_csv(file_a)
    source_b = pd.read_csv(file_b)
except Exception as e:
    st.error(f"Unable to read CSV file: {e}")
    st.stop()

required_columns = [
    "Order_ID",
    "Date",
    "Quantity",
    "Price",
    "Status",
]

missing_a = [col for col in required_columns if col not in source_a.columns]
missing_b = [col for col in required_columns if col not in source_b.columns]

if missing_a or missing_b:
    st.error("Required columns are missing.")

    if missing_a:
        st.write("Source A missing:", missing_a)

    if missing_b:
        st.write("Source B missing:", missing_b)

    st.stop()

# ============================================================
# CLEAN DATA
# ============================================================
source_a["Date"] = pd.to_datetime(source_a["Date"], errors="coerce")
source_b["Date"] = pd.to_datetime(source_b["Date"], errors="coerce")

source_a["Quantity"] = pd.to_numeric(
    source_a["Quantity"], errors="coerce"
).fillna(0)

source_b["Quantity"] = pd.to_numeric(
    source_b["Quantity"], errors="coerce"
).fillna(0)

source_a["Price"] = pd.to_numeric(
    source_a["Price"], errors="coerce"
).fillna(0)

source_b["Price"] = pd.to_numeric(
    source_b["Price"], errors="coerce"
).fillna(0)

# ============================================================
# SALES CALCULATION
# ============================================================
source_a["Sales"] = source_a["Quantity"] * source_a["Price"]
source_b["Sales"] = source_b["Quantity"] * source_b["Price"]

if "Discount" in source_a.columns:
    source_a["Discount"] = pd.to_numeric(
        source_a["Discount"], errors="coerce"
    ).fillna(0)
    source_a["Sales"] = (
        source_a["Quantity"] * source_a["Price"]
        - source_a["Discount"]
    )

if "Discount" in source_b.columns:
    source_b["Discount"] = pd.to_numeric(
        source_b["Discount"], errors="coerce"
    ).fillna(0)
    source_b["Sales"] = (
        source_b["Quantity"] * source_b["Price"]
        - source_b["Discount"]
    )

# ============================================================
# TOTALS
# ============================================================
sales_a = source_a["Sales"].sum()
sales_b = source_b["Sales"].sum()
difference = abs(sales_a - sales_b)

orders_a = set(source_a["Order_ID"].dropna())
orders_b = set(source_b["Order_ID"].dropna())

missing_in_b = orders_a - orders_b
missing_in_a = orders_b - orders_a

# ============================================================
# DUPLICATES
# ============================================================
duplicates_a = source_a[
    source_a.duplicated("Order_ID", keep=False)
]

duplicates_b = source_b[
    source_b.duplicated("Order_ID", keep=False)
]

# ============================================================
# DATE RANGE
# ============================================================
min_date_a = source_a["Date"].min()
max_date_a = source_a["Date"].max()

min_date_b = source_b["Date"].min()
max_date_b = source_b["Date"].max()

date_mismatch = (
    min_date_a != min_date_b
    or max_date_a != max_date_b
)

# ============================================================
# ISSUE DETECTION
# ============================================================
reasons = []

if missing_in_a or missing_in_b:
    reasons.append("Missing records")

if not duplicates_a.empty or not duplicates_b.empty:
    reasons.append("Duplicate records")

if date_mismatch:
    reasons.append("Different date ranges")

# ============================================================
# ORDER-LEVEL ROOT CAUSE ANALYSIS
# ============================================================
root_causes = []
comparison_rows = []

common_orders = orders_a.intersection(orders_b)

for order_id in common_orders:
    rows_a = source_a[source_a["Order_ID"] == order_id]
    rows_b = source_b[source_b["Order_ID"] == order_id]

    if rows_a.empty or rows_b.empty:
        continue

    row_a = rows_a.iloc[0]
    row_b = rows_b.iloc[0]

    quantity_diff = row_a["Quantity"] - row_b["Quantity"]
    price_diff = row_a["Price"] - row_b["Price"]
    sales_diff = row_a["Sales"] - row_b["Sales"]
    date_diff = row_a["Date"] != row_b["Date"]

    if (
        quantity_diff != 0
        or price_diff != 0
        or sales_diff != 0
        or date_diff
    ):
        comparison_rows.append(
            {
                "Order_ID": order_id,
                "A_Quantity": row_a["Quantity"],
                "B_Quantity": row_b["Quantity"],
                "A_Price": row_a["Price"],
                "B_Price": row_b["Price"],
                "A_Sales": row_a["Sales"],
                "B_Sales": row_b["Sales"],
                "Sales_Impact": abs(sales_diff),
                "Date_Mismatch": date_diff,
            }
        )

        if quantity_diff != 0:
            root_causes.append(
                {
                    "Order_ID": order_id,
                    "Cause": "Quantity mismatch",
                    "Impact": abs(sales_diff),
                }
            )

        if price_diff != 0:
            root_causes.append(
                {
                    "Order_ID": order_id,
                    "Cause": "Price mismatch",
                    "Impact": abs(sales_diff),
                }
            )

        if date_diff:
            root_causes.append(
                {
                    "Order_ID": order_id,
                    "Cause": "Order date mismatch",
                    "Impact": abs(sales_diff),
                }
            )

all_issues = reasons.copy()

if comparison_rows:
    all_issues.append("Order-level metric differences")

# ============================================================
# KPI RESULTS
# ============================================================
st.markdown(
    '<div class="section-title">📈 ANALYSIS RESULTS</div>',
    unsafe_allow_html=True,
)

k1, k2, k3, k4, k5 = st.columns(5)

kpis = [
    ("TOTAL SALES — SOURCE A", f"₹{sales_a:,.0f}", "Source A"),
    ("TOTAL SALES — SOURCE B", f"₹{sales_b:,.0f}", "Source B"),
    ("DIFFERENCE", f"₹{difference:,.0f}", "Absolute difference"),
    ("ISSUES FOUND", str(len(all_issues)), "Detected issue types"),
    ("ORDERS COMPARED", f"{len(orders_a | orders_b):,}", "Unique Order IDs"),
]

for col, (label, value, sub) in zip([k1, k2, k3, k4, k5], kpis):
    with col:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# VISUAL FLOW
# ============================================================

flow1, arrow1, flow2, arrow2, flow3 = st.columns(
    [2, 0.35, 2, 0.35, 2]
)

with flow1:
    st.markdown("## 🔍")
    st.markdown("**1. METRIC MISMATCH**")
    st.caption("Detect differences between two data sources")

with arrow1:
    st.markdown("## →")

with flow2:
    st.markdown("## 🧠")
    st.markdown("**2. ROOT CAUSE ANALYSIS**")
    st.caption("Identify the reasons behind the mismatch")

with arrow2:
    st.markdown("## →")

with flow3:
    st.markdown("## 💰")
    st.markdown("**3. FINANCIAL IMPACT**")
    st.caption("Calculate financial impact and insights")
    
# ============================================================
# DISCREPANCY + ROOT CAUSE
# ============================================================
st.markdown(
    '<div class="section-title">🔍 DISCREPANCY & ROOT CAUSE ANALYSIS</div>',
    unsafe_allow_html=True,
)

left, middle, right = st.columns([0.85, 1.55, 1.0], gap="large")

with left:
    st.markdown(
        """
        <div class="ui-card">
            <h3>🔎 Discrepancy Summary</h3>
        """,
        unsafe_allow_html=True,
    )

    if missing_in_a or missing_in_b:
        st.write(
            f"📌 Missing Records: "
            f"{len(missing_in_a) + len(missing_in_b)}"
        )

    if not duplicates_a.empty or not duplicates_b.empty:
        st.write(
            f"🔁 Duplicate Records: "
            f"{len(duplicates_a) + len(duplicates_b)}"
        )

    if date_mismatch:
        st.write("📅 Date Range Mismatch: Yes")

    if comparison_rows:
        st.write(
            f"🧮 Order-Level Differences: "
            f"{len(comparison_rows)}"
        )

    if not all_issues:
        st.success("No issues detected.")

    st.markdown("</div>", unsafe_allow_html=True)

with middle:
    st.markdown(
        """
        <div class="ui-card">
            <h3>📋 Discrepancy Details</h3>
        """,
        unsafe_allow_html=True,
    )

    if comparison_rows:
        comparison_df = pd.DataFrame(comparison_rows)

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("No order-level differences found.")

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    if root_causes:
        root_df = pd.DataFrame(root_causes)
        strongest = root_df.loc[root_df["Impact"].idxmax()]

        st.markdown("### 💡 Root Cause & Impact Insights")

        with st.container(border=True):
            st.markdown("**Main Root Cause**")
            st.write(strongest["Cause"])

            st.markdown("**Order**")
            st.write(strongest["Order_ID"])

            st.markdown("**Highest Impact**")
            st.markdown(f"### ₹{strongest["Impact"]:,.0f}")

            st.caption(
                "The strongest detected cause is highlighted for review."
            )

    elif missing_in_a or missing_in_b:
        st.markdown("### 💡 Root Cause & Impact Insights")

        with st.container(border=True):
            st.write("🔎 Root cause is related to missing records.")
            st.write(
                "Review records that exist in one source "
                "but not the other."
            )

    elif not duplicates_a.empty or not duplicates_b.empty:
        st.markdown("### 💡 Root Cause & Impact Insights")

        with st.container(border=True):
            st.write(
                "🔎 Root cause is related to duplicate records."
            )

    elif date_mismatch:
        st.markdown("### 💡 Root Cause & Impact Insights")

        with st.container(border=True):
            st.write(
                "🔎 Root cause is related to different date ranges."
            )

    else:
        st.markdown("### 💡 Root Cause & Impact Insights")

        with st.container(border=True):
            st.write("🟢 No root cause detected.")

# ============================================================
# CHARTS
# ============================================================
st.markdown(
    '<div class="section-title">📊 VISUAL ANALYSIS</div>',
    unsafe_allow_html=True,
)

chart1, chart2 = st.columns(2)

with chart1:
    st.markdown(
        '<div class="ui-card"><h3>Sales Comparison</h3>',
        unsafe_allow_html=True,
    )

    sales_chart = pd.DataFrame(
        {
            "Source A": [sales_a],
            "Source B": [sales_b],
        }
    )

    st.bar_chart(sales_chart)

    st.markdown("</div>", unsafe_allow_html=True)

with chart2:
    st.markdown(
        '<div class="ui-card"><h3>Issue Overview</h3>',
        unsafe_allow_html=True,
    )

    issue_chart = pd.DataFrame(
        {
            "Issue": [
                "Missing",
                "Duplicates",
                "Order Differences",
            ],
            "Count": [
                len(missing_in_a) + len(missing_in_b),
                len(duplicates_a) + len(duplicates_b),
                len(comparison_rows),
            ],
        }
    ).set_index("Issue")

    st.bar_chart(issue_chart)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# MISSING RECORDS
# ============================================================
if missing_in_b:
    st.markdown(
        '<div class="section-title">🔍 Orders Missing in Source B</div>',
        unsafe_allow_html=True,
    )

    missing_data = source_a[
        source_a["Order_ID"].isin(missing_in_b)
    ]

    st.dataframe(
        missing_data,
        use_container_width=True,
        hide_index=True,
    )

if missing_in_a:
    st.markdown(
        '<div class="section-title">🔍 Orders Missing in Source A</div>',
        unsafe_allow_html=True,
    )

    missing_data = source_b[
        source_b["Order_ID"].isin(missing_in_a)
    ]

    st.dataframe(
        missing_data,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# DUPLICATES
# ============================================================
if not duplicates_a.empty:
    st.markdown(
        '<div class="section-title">🔁 Duplicate Records in Source A</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        duplicates_a,
        use_container_width=True,
        hide_index=True,
    )

if not duplicates_b.empty:
    st.markdown(
        '<div class="section-title">🔁 Duplicate Records in Source B</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        duplicates_b,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# DATE CHECK
# ============================================================
st.markdown(
    '<div class="section-title">📅 DATE RANGE CHECK</div>',
    unsafe_allow_html=True,
)

d1, d2 = st.columns(2)

d1.markdown(
    f"""
    <div class="ui-card">
        <h3>Source A</h3>
        <p>{min_date_a.date()} → {max_date_a.date()}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

d2.markdown(
    f"""
    <div class="ui-card">
        <h3>Source B</h3>
        <p>{min_date_b.date()} → {max_date_b.date()}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if date_mismatch:
    st.warning("Date range mismatch detected.")
else:
    st.success("Date ranges are the same.")

# ============================================================
# FORMULA CHECK
# ============================================================
st.markdown(
    '<div class="section-title">🧮 FORMULA CHECK</div>',
    unsafe_allow_html=True,
)

formula1, formula2 = st.columns(2)

with formula1:
    st.markdown(
        """
        <div class="ui-card">
            <h3>Source A Calculation</h3>
            <p>Quantity × Price</p>
        """,
        unsafe_allow_html=True,
    )

    if "Discount" in source_a.columns:
        st.write("Discount is included.")

    st.markdown("</div>", unsafe_allow_html=True)

with formula2:
    st.markdown(
        """
        <div class="ui-card">
            <h3>Source B Calculation</h3>
        """,
        unsafe_allow_html=True,
    )

    if "Discount" in source_b.columns:
        st.write("Quantity × Price − Discount")

        if "Discount" not in source_a.columns:
            st.warning(
                "Calculation logic differs because Source B uses Discount."
            )
    else:
        st.write("Quantity × Price")

        if "Discount" not in source_a.columns:
            st.success("Same calculation logic detected.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FINAL RECOMMENDATION
# ============================================================
st.markdown(
    '<div class="section-title">🎯 FINAL RECOMMENDATION</div>',
    unsafe_allow_html=True,
)

if difference == 0 and not all_issues:
    st.success(
        "🟢 SAFE — Values match and no issues were detected."
    )

elif root_causes:
    strongest = root_df.loc[root_df["Impact"].idxmax()]

    st.error(
        f"🔴 ACTION REQUIRED — Check {strongest['Cause']} "
        f"for Order {strongest['Order_ID']}."
    )

    st.write(
        f"Estimated metric impact: "
        f"₹{strongest['Impact']:,.0f}"
    )

elif len(all_issues) == 1:
    st.warning(
        f"🟡 REVIEW REQUIRED — {all_issues[0]}"
    )

else:
    st.warning("🟡 HUMAN REVIEW REQUIRED")
    st.write(
        "Multiple factors may be causing the metric mismatch."
    )