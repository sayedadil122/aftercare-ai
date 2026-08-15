import streamlit as st
import pandas as pd
import plotly.express as px
from services.ui_fix import apply_html_fix
apply_html_fix()

st.set_page_config(
    page_title="Insights | AfterCare AI",
    page_icon="📊",
    layout="wide"
)

REPAIRS_FILE = "data/repairs.csv"
FOLLOWUPS_FILE = "data/followups.csv"
TICKETS_FILE = "data/tickets.csv"
RESOLUTIONS_FILE = "data/resolutions.csv"

repairs_df = pd.read_csv(REPAIRS_FILE)
followups_df = pd.read_csv(FOLLOWUPS_FILE)
tickets_df = pd.read_csv(TICKETS_FILE)
resolutions_df = pd.read_csv(RESOLUTIONS_FILE)

merged_df = followups_df.merge(
    repairs_df[
        [
            "repair_id",
            "device",
            "repair_type"
        ]
    ],
    on="repair_id",
    how="left"
)

completed_df = merged_df[
    merged_df["call_status"] == "Completed"
].copy()

issue_df = completed_df[
    completed_df["issue_detected"] == "Yes"
].copy()

healthy_df = completed_df[
    completed_df["health_status"] == "Healthy"
].copy()

negative_df = completed_df[
    completed_df["sentiment"] == "Negative"
].copy()

critical_df = completed_df[
    completed_df["severity"] == "Critical"
].copy()

resolved_df = resolutions_df[
    resolutions_df["status"] == "Resolved"
].copy()

reopened_df = resolutions_df[
    resolutions_df["status"] == "Reopened"
].copy()

completed_count = len(completed_df)

issue_rate = (
    round(
        (
            len(issue_df)
            / completed_count
        )
        * 100,
        1
    )
    if completed_count > 0
    else 0
)

healthy_rate = (
    round(
        (
            len(healthy_df)
            / completed_count
        )
        * 100,
        1
    )
    if completed_count > 0
    else 0
)

negative_rate = (
    round(
        (
            len(negative_df)
            / completed_count
        )
        * 100,
        1
    )
    if completed_count > 0
    else 0
)

recovery_total = len(
    resolutions_df
)

recovery_success_rate = (
    round(
        (
            len(resolved_df)
            / recovery_total
        )
        * 100,
        1
    )
    if recovery_total > 0
    else 0
)

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

    --blue: #1570EF;
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
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px;
    min-height: 122px;
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

.metric-foot {
    color: var(--muted);
    font-size: 12px;
    margin-top: 5px;
}

.metric-good {
    color: var(--green);
    font-size: 12px;
    font-weight: 650;
    margin-top: 5px;
}

.metric-danger {
    color: var(--red);
    font-size: 12px;
    font-weight: 650;
    margin-top: 5px;
}

.panel {
    background: white;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 20px;
    box-shadow:
        0 6px 22px
        rgba(
            16,
            24,
            40,
            0.04
        );
}

.section-title {
    color: var(--text);
    font-size: 18px;
    font-weight: 750;
    margin-bottom: 12px;
}

.ai-insight {
    background:
        linear-gradient(
            135deg,
            #F4F3FF 0%,
            #EEF4FF 100%
        );
    border: 1px solid #D9D6FE;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}

.ai-title {
    color: var(--text);
    font-size: 14px;
    font-weight: 750;
}

.ai-body {
    color: #475467;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 7px;
}

.risk-insight {
    background: var(--red-soft);
    border: 1px solid #FECDCA;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}

.success-insight {
    background: var(--green-soft);
    border: 1px solid #ABEFC6;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}

.warning-insight {
    background: var(--orange-soft);
    border: 1px solid #FEDF89;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}

.small {
    color: var(--muted);
    font-size: 12px;
}

.pattern-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #EAECF0;
}

.pattern-label {
    font-size: 13px;
    color: #344054;
    font-weight: 650;
}

.pattern-value {
    font-size: 13px;
    color: #101828;
    font-weight: 750;
}

.badge {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
}

.badge-purple {
    background: #F4F3FF;
    color: #6941C6;
}

.badge-red {
    background: #FEF3F2;
    color: #B42318;
}

.badge-green {
    background: #ECFDF3;
    color: #027A48;
}

div[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="page-title">Operations Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Turn post-service conversations into actionable patterns for service quality, technician operations and customer recovery.'
    '</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4, m5 = st.columns(5)

with m1:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            ISSUE RATE
        </div>

        <div class="metric-value">
            {issue_rate}%
        </div>

        <div class="metric-danger">
            {len(issue_df)} detected issue(s)
        </div>

    </div>
    """, unsafe_allow_html=True)

with m2:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            HEALTHY SERVICES
        </div>

        <div class="metric-value">
            {healthy_rate}%
        </div>

        <div class="metric-good">
            {len(healthy_df)} verified healthy
        </div>

    </div>
    """, unsafe_allow_html=True)

with m3:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            NEGATIVE SENTIMENT
        </div>

        <div class="metric-value">
            {negative_rate}%
        </div>

        <div class="metric-danger">
            {len(negative_df)} customer(s)
        </div>

    </div>
    """, unsafe_allow_html=True)

with m4:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            CRITICAL CASES
        </div>

        <div class="metric-value">
            {len(critical_df)}
        </div>

        <div class="metric-danger">
            Immediate attention
        </div>

    </div>
    """, unsafe_allow_html=True)

with m5:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            RECOVERY SUCCESS
        </div>

        <div class="metric-value">
            {recovery_success_rate}%
        </div>

        <div class="metric-good">
            {len(resolved_df)} resolved
        </div>

    </div>
    """, unsafe_allow_html=True)

st.write("")

chart1, chart2 = st.columns(
    2,
    gap="large"
)

with chart1:

    st.markdown(
        '<div class="section-title">Issues by Repair Type</div>',
        unsafe_allow_html=True
    )

    if not issue_df.empty:

        repair_issue_summary = (
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

        fig1 = px.bar(
            repair_issue_summary,
            x="repair_type",
            y="Issues"
        )

        fig1.update_layout(
            height=330,
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
            fig1,
            use_container_width=True
        )

    else:

        st.info(
            "No issue data available."
        )

with chart2:

    st.markdown(
        '<div class="section-title">Average Risk by Device</div>',
        unsafe_allow_html=True
    )

    device_risk = (
        completed_df.groupby(
            "device"
        )["risk_score"]
        .mean()
        .reset_index()
        .sort_values(
            "risk_score",
            ascending=False
        )
    )

    if not device_risk.empty:

        fig2 = px.bar(
            device_risk,
            x="device",
            y="risk_score"
        )

        fig2.update_layout(
            height=330,
            margin=dict(
                l=5,
                r=5,
                t=5,
                b=5
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="",
            yaxis_title="Average Risk Score",
            showlegend=False
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    else:

        st.info(
            "No device risk data available."
        )

st.write("")

chart3, chart4 = st.columns(
    2,
    gap="large"
)

with chart3:

    st.markdown(
        '<div class="section-title">Customer Sentiment</div>',
        unsafe_allow_html=True
    )

    sentiment_summary = (
        completed_df[
            "sentiment"
        ]
        .value_counts()
        .reset_index()
    )

    sentiment_summary.columns = [
        "Sentiment",
        "Customers"
    ]

    if not sentiment_summary.empty:

        sentiment_fig = px.pie(
            sentiment_summary,
            names="Sentiment",
            values="Customers",
            hole=0.58
        )

        sentiment_fig.update_layout(
            height=330,
            margin=dict(
                l=5,
                r=5,
                t=5,
                b=5
            )
        )

        st.plotly_chart(
            sentiment_fig,
            use_container_width=True
        )

    else:

        st.info(
            "No sentiment data available."
        )

with chart4:

    st.markdown(
        '<div class="section-title">Recovery Status</div>',
        unsafe_allow_html=True
    )

    recovery_summary = (
        resolutions_df[
            "status"
        ]
        .value_counts()
        .reset_index()
    )

    recovery_summary.columns = [
        "Status",
        "Cases"
    ]

    if not recovery_summary.empty:

        recovery_fig = px.bar(
            recovery_summary,
            x="Status",
            y="Cases"
        )

        recovery_fig.update_layout(
            height=330,
            margin=dict(
                l=5,
                r=5,
                t=5,
                b=5
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="",
            yaxis_title="Recovery Cases",
            showlegend=False
        )

        st.plotly_chart(
            recovery_fig,
            use_container_width=True
        )

    else:

        st.info(
            "No recovery data available."
        )

st.write("")

left, right = st.columns(
    [
        1.3,
        1
    ],
    gap="large"
)

with left:

    st.markdown(
        '<div class="section-title">🧠 AI Management Insights</div>',
        unsafe_allow_html=True
    )

    if not issue_df.empty:

        top_repair = (
            issue_df[
                "repair_type"
            ]
            .value_counts()
            .idxmax()
        )

        top_repair_count = (
            issue_df[
                "repair_type"
            ]
            .value_counts()
            .max()
        )

        st.markdown(f"""
        <div class="ai-insight">

            <span class="
                badge
                badge-purple
            ">
                PATTERN DETECTED
            </span>

            <br><br>

            <div class="ai-title">
                {top_repair} is generating the most post-service issues
            </div>

            <div class="ai-body">
                {top_repair_count} detected issue case(s)
                are associated with this repair category.

                Review technician SOP, replacement-part quality
                and common failure modes before treating this
                as a confirmed root cause.
            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="success-insight">

            <div class="ai-title">
                ✅ No recurring repair issue detected
            </div>

            <div class="ai-body">
                Current follow-up data does not show a recurring
                post-service failure pattern.
            </div>

        </div>
        """, unsafe_allow_html=True)

    if not completed_df.empty:

        highest_risk_row = (
            completed_df.sort_values(
                "risk_score",
                ascending=False
            )
            .iloc[0]
        )

        st.markdown(f"""
        <div class="risk-insight">

            <span class="
                badge
                badge-red
            ">
                HIGHEST RISK
            </span>

            <br><br>

            <div class="ai-title">
                {highest_risk_row["customer_name"]}
                •
                {highest_risk_row["device"]}
            </div>

            <div class="ai-body">
                Risk Score:
                <b>
                    {highest_risk_row["risk_score"]}/100
                </b>

                <br>

                Severity:
                <b>
                    {highest_risk_row["severity"]}
                </b>

                <br>

                Recommended Action:
                <b>
                    {highest_risk_row["recommended_action"]}
                </b>
            </div>

        </div>
        """, unsafe_allow_html=True)

    if not negative_df.empty:

        st.markdown(f"""
        <div class="warning-insight">

            <div class="ai-title">
                ⚠️ Customer experience risk detected
            </div>

            <div class="ai-body">
                {len(negative_df)} completed follow-up(s)
                contain negative customer sentiment.

                Prioritize these cases even when the technical
                severity is not critical, because dissatisfaction
                can lead to repeat complaints or churn.
            </div>

        </div>
        """, unsafe_allow_html=True)

with right:

    st.markdown(
        '<div class="section-title">Operational Patterns</div>',
        unsafe_allow_html=True
    )

    if not completed_df.empty:

        top_device = (
            completed_df.sort_values(
                "risk_score",
                ascending=False
            )
            .iloc[0]["device"]
        )

        avg_risk = round(
            completed_df[
                "risk_score"
            ].mean(),
            1
        )

        warranty_cases = len(
            tickets_df[
                tickets_df[
                    "warranty_review"
                ].isin(
                    [
                        "Recommended",
                        "Required"
                    ]
                )
            ]
        )

        patterns_html = f"""
        <div class="panel">

            <div class="pattern-row">

                <div class="pattern-label">
                    Average Service Risk
                </div>

                <div class="pattern-value">
                    {avg_risk}/100
                </div>

            </div>

            <div class="pattern-row">

                <div class="pattern-label">
                    Highest-Risk Device
                </div>

                <div class="pattern-value">
                    {top_device}
                </div>

            </div>

            <div class="pattern-row">

                <div class="pattern-label">
                    Warranty Review Cases
                </div>

                <div class="pattern-value">
                    {warranty_cases}
                </div>

            </div>

            <div class="pattern-row">

                <div class="pattern-label">
                    Reopened Recovery Cases
                </div>

                <div class="pattern-value">
                    {len(reopened_df)}
                </div>

            </div>

            <div class="pattern-row">

                <div class="pattern-label">
                    Successful Recoveries
                </div>

                <div class="pattern-value">
                    {len(resolved_df)}
                </div>

            </div>

        </div>
        """

        st.markdown(
            patterns_html,
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown(
        '<div class="section-title">Founder View</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="ai-insight">

        <div class="ai-title">
            What should operations investigate next?
        </div>

        <div class="ai-body">

            1. Review repair categories with repeated issues.

            <br><br>

            2. Compare device-level risk against parts and technician data.

            <br><br>

            3. Prioritize negative-sentiment cases before customers
            contact support again.

            <br><br>

            4. Track whether recovery actions actually improve final CSAT.

        </div>

    </div>
    """, unsafe_allow_html=True)

st.write("")

st.markdown(
    '<div class="section-title">High-Risk Customer Cases</div>',
    unsafe_allow_html=True
)

high_risk_display = (
    completed_df[
        completed_df[
            "risk_score"
        ] >= 60
    ][
        [
            "customer_name",
            "device",
            "repair_type",
            "severity",
            "sentiment",
            "risk_score",
            "recommended_action"
        ]
    ]
    .copy()
)

high_risk_display.columns = [
    "Customer",
    "Device",
    "Repair",
    "Severity",
    "Sentiment",
    "Risk Score",
    "AI Action"
]

if high_risk_display.empty:

    st.success(
        "No high-risk customer cases in the current dataset."
    )

else:

    st.dataframe(
        high_risk_display,
        use_container_width=True,
        hide_index=True
    )

st.write("")

st.caption(
    "AfterCare AI • Operations Intelligence Engine"
)