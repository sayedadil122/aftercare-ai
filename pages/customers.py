import streamlit as st
import pandas as pd
from services.ui_fix import apply_html_fix
apply_html_fix()

st.set_page_config(
    page_title="Customers | AfterCare AI",
    page_icon="👥",
    layout="wide"
)

CUSTOMERS_FILE = "data/customers.csv"
REPAIRS_FILE = "data/repairs.csv"
FOLLOWUPS_FILE = "data/followups.csv"
TICKETS_FILE = "data/tickets.csv"
RESOLUTIONS_FILE = "data/resolutions.csv"

customers_df = pd.read_csv(CUSTOMERS_FILE)
repairs_df = pd.read_csv(REPAIRS_FILE)
followups_df = pd.read_csv(FOLLOWUPS_FILE)
tickets_df = pd.read_csv(TICKETS_FILE)
resolutions_df = pd.read_csv(RESOLUTIONS_FILE)

st.markdown("""
<style>

:root {
    --bg: #F5F7FB;
    --surface: #FFFFFF;
    --text: #101828;
    --muted: #667085;
    --border: #EAECF0;
    --purple: #7F56D9;
    --purple-soft: #F4F3FF;
    --green: #039855;
    --green-soft: #ECFDF3;
    --orange: #DC6803;
    --orange-soft: #FFFAEB;
    --red: #D92D20;
    --red-soft: #FEF3F2;
    --blue-soft: #EFF8FF;
}

.stApp {
    background: var(--bg);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.7rem;
    padding-bottom: 3rem;
}

.page-title {
    font-size: 34px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.03em;
    line-height: 1.15;
}

.page-subtitle {
    color: var(--muted);
    font-size: 14px;
    margin-top: 7px;
    margin-bottom: 26px;
}

.metric-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px;
    box-shadow:
        0 6px 22px
        rgba(
            16,
            24,
            40,
            0.04
        );
}

.metric-label {
    color: var(--muted);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
}

.metric-value {
    color: var(--text);
    font-size: 30px;
    font-weight: 800;
    margin-top: 7px;
}

.customer-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow:
        0 6px 22px
        rgba(
            16,
            24,
            40,
            0.04
        );
}

.customer-name {
    font-size: 19px;
    font-weight: 750;
    color: var(--text);
}

.customer-sub {
    font-size: 12px;
    color: var(--muted);
    margin-top: 3px;
}

.info-grid {
    display: grid;
    grid-template-columns:
        repeat(
            4,
            minmax(
                0,
                1fr
            )
        );
    gap: 14px;
    margin-top: 18px;
}

.info-box {
    background: #F9FAFB;
    border: 1px solid #F2F4F7;
    border-radius: 14px;
    padding: 13px;
}

.info-label {
    color: var(--muted);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.04em;
}

.info-value {
    color: var(--text);
    font-size: 13px;
    font-weight: 650;
    margin-top: 4px;
}

.badge {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
}

.badge-healthy {
    background: var(--green-soft);
    color: #027A48;
}

.badge-risk {
    background: var(--orange-soft);
    color: #B54708;
}

.badge-critical {
    background: var(--red-soft);
    color: #B42318;
}

.badge-pending {
    background: var(--blue-soft);
    color: #175CD3;
}

.ai-panel {
    background:
        linear-gradient(
            135deg,
            #F4F3FF 0%,
            #EEF4FF 100%
        );
    border: 1px solid #D9D6FE;
    border-radius: 18px;
    padding: 18px;
}

.section-title {
    font-size: 18px;
    font-weight: 750;
    color: var(--text);
    margin-bottom: 12px;
}

.small {
    color: var(--muted);
    font-size: 12px;
}

div[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="page-title">Customer Service Health</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Monitor customer repair history, post-service health and recovery risk across the service lifecycle.'
    '</div>',
    unsafe_allow_html=True
)

total_customers = len(customers_df)

healthy_customers = len(
    customers_df[
        customers_df["customer_status"] == "Healthy"
    ]
)

at_risk_customers = len(
    customers_df[
        customers_df["customer_status"] == "At Risk"
    ]
)

critical_customers = len(
    customers_df[
        customers_df["customer_status"] == "Critical"
    ]
)

pending_customers = len(
    customers_df[
        customers_df["customer_status"] == "Pending Follow-up"
    ]
)

m1, m2, m3, m4, m5 = st.columns(5)

metrics = [
    ("TOTAL CUSTOMERS", total_customers),
    ("HEALTHY", healthy_customers),
    ("AT RISK", at_risk_customers),
    ("CRITICAL", critical_customers),
    ("PENDING FOLLOW-UP", pending_customers)
]

for col, item in zip(
    [m1, m2, m3, m4, m5],
    metrics
):
    with col:
        st.markdown(f"""
        <div class="metric-card">

            <div class="metric-label">
                {item[0]}
            </div>

            <div class="metric-value">
                {item[1]}
            </div>

        </div>
        """, unsafe_allow_html=True)

st.write("")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    health_filter = st.selectbox(
        "Filter by Customer Health",
        [
            "All",
            "Healthy",
            "At Risk",
            "Critical",
            "Pending Follow-up"
        ]
    )

with filter_col2:
    search_customer = st.text_input(
        "Search Customer",
        placeholder="Search by customer name..."
    )

filtered_df = customers_df.copy()

if health_filter != "All":
    filtered_df = filtered_df[
        filtered_df["customer_status"] == health_filter
    ]

if search_customer.strip():
    filtered_df = filtered_df[
        filtered_df["customer_name"]
        .astype(str)
        .str.contains(
            search_customer,
            case=False,
            na=False
        )
    ]

st.write("")

st.markdown(
    '<div class="section-title">Customer Health Profiles</div>',
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.info(
        "No customers match the selected filters."
    )

else:

    for _, customer in filtered_df.iterrows():

        customer_name = customer["customer_name"]

        customer_repairs = repairs_df[
            repairs_df["customer_name"] == customer_name
        ]

        customer_followups = followups_df[
            followups_df["customer_name"] == customer_name
        ]

        customer_tickets = tickets_df[
            tickets_df["customer_name"] == customer_name
        ]

        customer_ticket_ids = (
            customer_tickets["ticket_id"]
            .astype(str)
            .tolist()
            if not customer_tickets.empty
            else []
        )

        customer_recovery = resolutions_df[
            resolutions_df["ticket_id"].isin(
                customer_ticket_ids
            )
        ]

        if not customer_followups.empty:
            latest_followup = (
                customer_followups
                .sort_values(
                    by="scheduled_at",
                    ascending=False
                )
                .iloc[0]
            )

            latest_risk = latest_followup["risk_score"]
            latest_health = latest_followup["health_status"]
            latest_action = latest_followup["recommended_action"]

        else:
            latest_risk = 0
            latest_health = "Pending"
            latest_action = "Awaiting AI Follow-up"

        status = customer["customer_status"]

        status_class = {
            "Healthy": "badge-healthy",
            "At Risk": "badge-risk",
            "Critical": "badge-critical",
            "Pending Follow-up": "badge-pending"
        }.get(
            status,
            "badge-pending"
        )

        open_tickets = len(
            customer_tickets[
                customer_tickets["status"].isin(
                    ["Open", "Escalated"]
                )
            ]
        )

        active_recoveries = len(
            customer_recovery[
                customer_recovery["status"].isin(
                    [
                        "Scheduled",
                        "In Progress",
                        "Reopened"
                    ]
                )
            ]
        )

        st.markdown(f"""
        <div class="customer-card">

            <span class="
                badge
                {status_class}
            ">
                {status}
            </span>

            <br><br>

            <div class="customer-name">
                {customer_name}
            </div>

            <div class="customer-sub">
                {customer["phone"]}
                •
                {customer["email"]}
            </div>

            <div class="info-grid">

                <div class="info-box">

                    <div class="info-label">
                        TOTAL REPAIRS
                    </div>

                    <div class="info-value">
                        {customer["total_repairs"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        LAST DEVICE
                    </div>

                    <div class="info-value">
                        {customer["last_device"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        LAST REPAIR
                    </div>

                    <div class="info-value">
                        {customer["last_repair_type"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        LAST SERVICE
                    </div>

                    <div class="info-value">
                        {customer["last_service_date"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        LATEST AI HEALTH
                    </div>

                    <div class="info-value">
                        {latest_health}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        LATEST RISK SCORE
                    </div>

                    <div class="info-value">
                        {latest_risk}/100
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        OPEN TICKETS
                    </div>

                    <div class="info-value">
                        {open_tickets}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        ACTIVE RECOVERIES
                    </div>

                    <div class="info-value">
                        {active_recoveries}
                    </div>

                </div>

            </div>

            <br>

            <div class="info-label">
                AI RECOMMENDED ACTION
            </div>

            <div class="info-value">
                {latest_action}
            </div>

        </div>
        """, unsafe_allow_html=True)

st.write("")

left, right = st.columns(
    [1.2, 1],
    gap="large"
)

with left:

    st.markdown(
        '<div class="section-title">Customer Risk Distribution</div>',
        unsafe_allow_html=True
    )

    status_summary = (
        customers_df[
            "customer_status"
        ]
        .value_counts()
        .reset_index()
    )

    status_summary.columns = [
        "Customer Status",
        "Customers"
    ]

    st.dataframe(
        status_summary,
        use_container_width=True,
        hide_index=True
    )

with right:

    st.markdown(
        '<div class="section-title">🧠 AI Customer Health Insight</div>',
        unsafe_allow_html=True
    )

    if critical_customers > 0:

        recommendation = (
            f"{critical_customers} customer(s) are currently marked critical. "
            f"Prioritize these cases for immediate recovery and verify resolution "
            f"before considering the service relationship healthy."
        )

    elif at_risk_customers > 0:

        recommendation = (
            f"{at_risk_customers} customer(s) are currently at risk. "
            f"Review open tickets, negative sentiment and pending recovery actions "
            f"before they create repeat support contacts."
        )

    elif pending_customers > 0:

        recommendation = (
            f"{pending_customers} customer(s) are still waiting for an AI follow-up. "
            f"Complete the post-service verification before assigning final health status."
        )

    else:

        recommendation = (
            "Current customer base is healthy. Continue monitoring post-service "
            "follow-ups and watch for repeat issues or negative sentiment."
        )

    st.markdown(f"""
    <div class="ai-panel">

        <b>
            Customer Health Recommendation
        </b>

        <br><br>

        <span class="small">
            {recommendation}
        </span>

    </div>
    """, unsafe_allow_html=True)

st.write("")

st.markdown(
    '<div class="section-title">All Customer Data</div>',
    unsafe_allow_html=True
)

st.dataframe(
    customers_df,
    use_container_width=True,
    hide_index=True
)

st.write("")

st.caption(
    "AfterCare AI • Customer Service Health Intelligence"
)