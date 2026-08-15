import streamlit as st
import pandas as pd
import plotly.express as px
from services.ui_fix import apply_html_fix
apply_html_fix()

st.set_page_config(
    page_title="Issues | AfterCare AI",
    page_icon="⚠️",
    layout="wide"
)

FOLLOWUPS_FILE = "data/followups.csv"
REPAIRS_FILE = "data/repairs.csv"
TICKETS_FILE = "data/tickets.csv"

followups_df = pd.read_csv(FOLLOWUPS_FILE)
repairs_df = pd.read_csv(REPAIRS_FILE)
tickets_df = pd.read_csv(TICKETS_FILE)

merged_df = followups_df.merge(
    repairs_df[
        [
            "repair_id",
            "device",
            "repair_type",
            "phone",
            "completed_at"
        ]
    ],
    on="repair_id",
    how="left"
)

issue_df = merged_df[
    merged_df["issue_detected"] == "Yes"
].copy()

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
    --green-soft: #ECFDF3;
    --orange-soft: #FFFAEB;
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
    box-shadow: 0 6px 22px rgba(16, 24, 40, 0.04);
}

.metric-label {
    color: var(--muted);
    font-size: 11px;
    font-weight: 700;
}

.metric-value {
    color: var(--text);
    font-size: 30px;
    font-weight: 800;
    margin-top: 7px;
}

.issue-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 6px 22px rgba(16, 24, 40, 0.04);
}

.customer-name {
    font-size: 19px;
    font-weight: 750;
    color: var(--text);
}

.customer-sub {
    color: var(--muted);
    font-size: 12px;
    margin-top: 3px;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
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
    margin-right: 6px;
}

.badge-critical {
    background: var(--red-soft);
    color: #B42318;
}

.badge-high {
    background: var(--orange-soft);
    color: #B54708;
}

.badge-medium {
    background: var(--blue-soft);
    color: #175CD3;
}

.badge-low {
    background: var(--green-soft);
    color: #027A48;
}

.ai-panel {
    background: linear-gradient(
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
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="page-title">Detected Service Issues</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Review customer-reported post-service problems, risk signals and AI-recommended recovery actions.'
    '</div>',
    unsafe_allow_html=True
)

total_issues = len(issue_df)

critical_issues = len(
    issue_df[
        issue_df["severity"] == "Critical"
    ]
)

high_issues = len(
    issue_df[
        issue_df["severity"] == "High"
    ]
)

negative_issues = len(
    issue_df[
        issue_df["sentiment"] == "Negative"
    ]
)

avg_risk = (
    round(
        issue_df["risk_score"].mean(),
        1
    )
    if not issue_df.empty
    else 0
)

m1, m2, m3, m4, m5 = st.columns(5)

metrics = [
    ("TOTAL ISSUES", total_issues),
    ("CRITICAL", critical_issues),
    ("HIGH SEVERITY", high_issues),
    ("NEGATIVE SENTIMENT", negative_issues),
    ("AVG RISK", f"{avg_risk}/100")
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

f1, f2 = st.columns(2)

with f1:
    severity_filter = st.selectbox(
        "Filter by Severity",
        [
            "All",
            "Critical",
            "High",
            "Medium",
            "Low"
        ]
    )

with f2:
    sentiment_filter = st.selectbox(
        "Filter by Sentiment",
        [
            "All",
            "Negative",
            "Neutral",
            "Positive"
        ]
    )

filtered_df = issue_df.copy()

if severity_filter != "All":
    filtered_df = filtered_df[
        filtered_df["severity"] == severity_filter
    ]

if sentiment_filter != "All":
    filtered_df = filtered_df[
        filtered_df["sentiment"] == sentiment_filter
    ]

st.write("")

st.markdown(
    '<div class="section-title">Active Issue Cases</div>',
    unsafe_allow_html=True
)

if filtered_df.empty:

    st.success(
        "No detected issues match the selected filters."
    )

else:

    for _, row in filtered_df.iterrows():

        severity_class = {
            "Critical": "badge-critical",
            "High": "badge-high",
            "Medium": "badge-medium",
            "Low": "badge-low"
        }.get(
            row["severity"],
            "badge-low"
        )

        ticket_match = tickets_df[
            tickets_df["repair_id"] == row["repair_id"]
        ]

        if not ticket_match.empty:
            ticket_id = ticket_match.iloc[0]["ticket_id"]
            ticket_status = ticket_match.iloc[0]["status"]
        else:
            ticket_id = "Not Created"
            ticket_status = "Pending"

        st.markdown(f"""
        <div class="issue-card">

            <span class="
                badge
                {severity_class}
            ">
                {row["severity"]}
            </span>

            <br><br>

            <div class="customer-name">
                {row["customer_name"]}
            </div>

            <div class="customer-sub">
                {row["device"]}
                •
                {row["repair_type"]}
            </div>

            <div class="info-grid">

                <div class="info-box">

                    <div class="info-label">
                        REPAIR ID
                    </div>

                    <div class="info-value">
                        {row["repair_id"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        RISK SCORE
                    </div>

                    <div class="info-value">
                        {row["risk_score"]}/100
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        SENTIMENT
                    </div>

                    <div class="info-value">
                        {row["sentiment"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        HEALTH STATUS
                    </div>

                    <div class="info-value">
                        {row["health_status"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        TICKET
                    </div>

                    <div class="info-value">
                        {ticket_id}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        TICKET STATUS
                    </div>

                    <div class="info-value">
                        {ticket_status}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        SERVICE COMPLETED
                    </div>

                    <div class="info-value">
                        {row["completed_at"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        AI ACTION
                    </div>

                    <div class="info-value">
                        {row["recommended_action"]}
                    </div>

                </div>

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
        '<div class="section-title">Issue Pattern by Repair Type</div>',
        unsafe_allow_html=True
    )

    if issue_df.empty:

        st.info(
            "No issue data available."
        )

    else:

        issue_summary = (
            issue_df.groupby(
                "repair_type"
            )
            .size()
            .reset_index(
                name="Issues"
            )
            .sort_values(
                "Issues",
                ascending=False
            )
        )

        fig = px.bar(
            issue_summary,
            x="repair_type",
            y="Issues"
        )

        fig.update_layout(
            height=320,
            margin=dict(
                l=5,
                r=5,
                t=5,
                b=5
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="",
            yaxis_title="Detected Issues",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with right:

    st.markdown(
        '<div class="section-title">🧠 AI Operations Insight</div>',
        unsafe_allow_html=True
    )

    if critical_issues > 0:

        recommendation = (
            f"{critical_issues} critical issue case(s) are active. "
            f"These should bypass normal support queues and move directly "
            f"to senior technician or human escalation."
        )

    elif high_issues > 0:

        recommendation = (
            f"{high_issues} high-severity issue case(s) are active. "
            f"Prioritize technician revisits and validate whether the "
            f"problem is related to the recently repaired component."
        )

    elif total_issues > 0:

        recommendation = (
            "Post-service issues are present but no critical pattern "
            "is currently dominant. Continue monitoring risk scores, "
            "repeat complaints and customer sentiment."
        )

    else:

        recommendation = (
            "No active post-service issues are currently detected."
        )

    st.markdown(f"""
    <div class="ai-panel">

        <b>
            Recommended Operational Focus
        </b>

        <br><br>

        <span class="small">
            {recommendation}
        </span>

    </div>
    """, unsafe_allow_html=True)

st.write("")

st.markdown(
    '<div class="section-title">All Detected Issue Data</div>',
    unsafe_allow_html=True
)

if issue_df.empty:

    st.info(
        "No detected issue records available."
    )

else:

    display_df = issue_df[
        [
            "customer_name",
            "device",
            "repair_type",
            "severity",
            "sentiment",
            "risk_score",
            "recommended_action"
        ]
    ].copy()

    display_df.columns = [
        "Customer",
        "Device",
        "Repair",
        "Severity",
        "Sentiment",
        "Risk Score",
        "AI Action"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

st.write("")

st.caption(
    "AfterCare AI • Post-Service Issue Intelligence"
)