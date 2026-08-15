import streamlit as st
import pandas as pd
import plotly.express as px

from services.scheduler import (
    get_due_followups,
    get_next_followups
)

from services.automation import (
    process_due_followups
)


st.set_page_config(
    page_title="AfterCare AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


REPAIRS_FILE = "data/repairs.csv"
FOLLOWUPS_FILE = "data/followups.csv"
TICKETS_FILE = "data/tickets.csv"
CUSTOMERS_FILE = "data/customers.csv"
RESOLUTIONS_FILE = "data/resolutions.csv"


def safe_read_csv(file_path):

    try:
        return pd.read_csv(file_path)

    except Exception:
        return pd.DataFrame()


repairs_df = safe_read_csv(
    REPAIRS_FILE
)

followups_df = safe_read_csv(
    FOLLOWUPS_FILE
)

tickets_df = safe_read_csv(
    TICKETS_FILE
)

customers_df = safe_read_csv(
    CUSTOMERS_FILE
)

resolutions_df = safe_read_csv(
    RESOLUTIONS_FILE
)


completed_followups = (
    len(
        followups_df[
            followups_df["call_status"]
            == "Completed"
        ]
    )
    if not followups_df.empty
    else 0
)


issues_detected = (
    len(
        followups_df[
            followups_df["issue_detected"]
            == "Yes"
        ]
    )
    if not followups_df.empty
    else 0
)


critical_cases = (
    len(
        followups_df[
            followups_df["severity"]
            == "Critical"
        ]
    )
    if not followups_df.empty
    else 0
)


healthy_cases = (
    len(
        followups_df[
            followups_df["health_status"]
            == "Healthy"
        ]
    )
    if not followups_df.empty
    else 0
)


if completed_followups > 0:

    service_health = round(
        (
            healthy_cases
            / completed_followups
        )
        * 100
    )

else:

    service_health = 0


try:

    due_followups_df = (
        get_due_followups()
    )

except Exception:

    due_followups_df = (
        pd.DataFrame()
    )


try:

    upcoming_followups_df = (
        get_next_followups()
    )

except Exception:

    upcoming_followups_df = (
        pd.DataFrame()
    )


resolved_cases = (
    len(
        resolutions_df[
            resolutions_df["status"]
            == "Resolved"
        ]
    )
    if not resolutions_df.empty
    else 0
)


open_recovery_cases = (
    len(
        resolutions_df[
            resolutions_df["status"].isin(
                [
                    "Scheduled",
                    "In Progress",
                    "Reopened"
                ]
            )
        ]
    )
    if not resolutions_df.empty
    else 0
)


st.markdown(
    """
    <style>

    :root {
        --bg: #F5F7FB;
        --surface: #FFFFFF;
        --text: #101828;
        --muted: #667085;
        --border: #EAECF0;
        --sidebar: #101828;
        --purple: #7F56D9;
        --purple-soft: #F4F3FF;
        --green: #039855;
        --green-soft: #ECFDF3;
        --orange: #DC6803;
        --orange-soft: #FFFAEB;
        --red: #D92D20;
        --red-soft: #FEF3F2;
    }

    .stApp {
        background: var(--bg);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #101828 0%,
                #172033 100%
            );
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 5px 0 8px 0;
    }

    .brand-icon {
        width: 42px;
        height: 42px;
        border-radius: 13px;
        background:
            linear-gradient(
                135deg,
                #7F56D9,
                #6941C6
            );
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 21px;
    }

    .brand-title {
        font-size: 20px;
        font-weight: 800;
        color: white;
    }

    .brand-sub {
        font-size: 11px;
        color: #98A2B3;
        margin-top: 2px;
    }

    .hero-wrap {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        color: #101828;
        letter-spacing: -0.03em;
        line-height: 1.15;
    }

    .hero-sub {
        color: #667085;
        font-size: 14px;
        margin-top: 8px;
    }

    .live-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #ECFDF3;
        color: #027A48;
        border: 1px solid #ABEFC6;
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #12B76A;
    }

    .metric-card {
        background: white;
        border: 1px solid #EAECF0;
        border-radius: 18px;
        padding: 18px;
        min-height: 120px;
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
        color: #667085;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    .metric-value {
        color: #101828;
        font-size: 31px;
        font-weight: 800;
        margin-top: 8px;
    }

    .metric-foot {
        color: #039855;
        font-size: 12px;
        font-weight: 600;
        margin-top: 5px;
    }

    .metric-danger {
        color: #D92D20;
        font-size: 12px;
        font-weight: 600;
        margin-top: 5px;
    }

    .section-title {
        font-size: 18px;
        font-weight: 750;
        color: #101828;
        margin-bottom: 12px;
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

    .panel {
        background: white;
        border: 1px solid #EAECF0;
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

    .alert {
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 10px;
    }

    .alert-red {
        background: #FEF3F2;
        border: 1px solid #FECDCA;
    }

    .alert-orange {
        background: #FFFAEB;
        border: 1px solid #FEDF89;
    }

    .alert-purple {
        background: #F4F3FF;
        border: 1px solid #D9D6FE;
    }

    .small {
        color: #667085;
        font-size: 12px;
        line-height: 1.55;
    }

    .case-name {
        font-size: 20px;
        font-weight: 750;
        color: #101828;
    }

    .case-risk {
        font-size: 40px;
        font-weight: 800;
        color: #D92D20;
        margin-top: 4px;
    }

    .flow-step {
        display: flex;
        gap: 12px;
        margin-bottom: 13px;
        align-items: flex-start;
    }

    .flow-num {
        min-width: 30px;
        height: 30px;
        border-radius: 10px;
        background: #F4F3FF;
        color: #7F56D9;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 11px;
        font-weight: 800;
    }

    .flow-title {
        font-size: 13px;
        font-weight: 700;
        color: #101828;
    }

    .flow-sub {
        font-size: 12px;
        color: #667085;
        margin-top: 2px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #EAECF0;
        border-radius: 16px;
        padding: 14px 16px;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
    }

    button {
        border-radius: 12px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:

    st.html(
        """
        <div class="brand-row">

            <div class="brand-icon">
                🤖
            </div>

            <div>

                <div class="brand-title">
                    AfterCare AI
                </div>

                <div class="brand-sub">
                    Autonomous Service Recovery
                </div>

            </div>

        </div>
        """
    )

    st.markdown("---")

    st.page_link(
        "app.py",
        label="Dashboard",
        icon="🏠"
    )

    st.page_link(
        "pages/new_service.py",
        label="New Service",
        icon="➕"
    )

    st.page_link(
        "pages/followups.py",
        label="Follow-up Calls",
        icon="📞"
    )

    st.page_link(
        "pages/issues.py",
        label="Issues",
        icon="⚠️"
    )

    st.page_link(
        "pages/tickets.py",
        label="Tickets",
        icon="🎫"
    )

    st.page_link(
        "pages/recovery_center.py",
        label="Recovery Center",
        icon="🛠️"
    )

    st.page_link(
        "pages/customers.py",
        label="Customers",
        icon="👥"
    )

    st.page_link(
        "pages/case_detail.py",
        label="Case Intelligence",
        icon="🧠"
    )

    st.page_link(
        "pages/insights.py",
        label="Insights",
        icon="📊"
    )

    st.page_link(
        "pages/settings.py",
        label="Settings",
        icon="⚙️"
    )

    st.markdown("---")

    st.success(
        "● Automation Online"
    )

    st.caption(
        "Simulation Mode"
    )

    if st.button(
        "Run Due Follow-ups",
        use_container_width=True
    ):

        try:

            results = (
                process_due_followups(
                    test_mode=True
                )
            )

            if results:

                st.success(
                    f"{len(results)} follow-up(s) processed."
                )

                st.rerun()

            else:

                st.info(
                    "No new due follow-ups."
                )

        except Exception as e:

            st.error(
                f"Automation error: {e}"
            )


st.html(
    """
    <div class="hero-wrap">

        <div>

            <div class="hero-title">
                Service Recovery Command Center
            </div>

            <div class="hero-sub">
                Monitor customer health, AI follow-ups,
                tickets and recovery operations in real time.
            </div>

        </div>

        <div class="live-pill">

            <div class="live-dot"></div>

            AI Operations Live

        </div>

    </div>
    """
)


m1, m2, m3, m4, m5 = st.columns(
    5
)


with m1:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                SERVICE HEALTH
            </div>

            <div class="metric-value">
                {service_health}%
            </div>

            <div class="metric-foot">
                Based on completed calls
            </div>

        </div>
        """
    )


with m2:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                FOLLOW-UPS COMPLETED
            </div>

            <div class="metric-value">
                {completed_followups}
            </div>

            <div class="metric-foot">
                {len(followups_df)} total follow-ups
            </div>

        </div>
        """
    )


with m3:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                ISSUES DETECTED
            </div>

            <div class="metric-value">
                {issues_detected}
            </div>

            <div class="metric-danger">
                Needs service attention
            </div>

        </div>
        """
    )


with m4:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                CRITICAL CASES
            </div>

            <div class="metric-value">
                {critical_cases}
            </div>

            <div class="metric-danger">
                Immediate escalation
            </div>

        </div>
        """
    )


with m5:

    st.html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                RECOVERY CASES
            </div>

            <div class="metric-value">
                {len(resolutions_df)}
            </div>

            <div class="metric-foot">
                {resolved_cases} resolved
            </div>

        </div>
        """
    )


st.write("")


a1, a2, a3 = st.columns(
    [
        1.6,
        1,
        1
    ]
)


with a1:

    st.html(
        """
        <div class="ai-panel">

            <b style="
                font-size:16px;
                color:#101828;
            ">
                ⚡ Autonomous Follow-up Engine
            </b>

            <br><br>

            <span class="small">
                Completed services are monitored automatically.
                Follow-up timing changes by repair type and
                detected issues move into ticket and recovery workflows.
            </span>

        </div>
        """
    )


with a2:

    st.metric(
        "Calls Due Now",
        len(due_followups_df)
    )


with a3:

    st.metric(
        "Upcoming Calls",
        len(upcoming_followups_df)
    )


st.write("")


chart_col, attention_col = st.columns(
    [
        2,
        1
    ]
)


with chart_col:

    st.html(
        """
        <div class="section-title">
            Service Health Trend
        </div>
        """
    )

    health_data = pd.DataFrame(
        {
            "Day": [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ],
            "Health": [
                82,
                84,
                86,
                85,
                88,
                90,
                91
            ]
        }
    )

    fig = px.line(
        health_data,
        x="Day",
        y="Health",
        markers=True
    )

    fig.update_traces(
        line_width=3,
        marker_size=8
    )

    fig.update_layout(
        height=310,
        margin=dict(
            l=5,
            r=5,
            t=5,
            b=5
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="",
        yaxis_title="Health %",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with attention_col:

    warranty_count = 0

    if not tickets_df.empty:

        if "warranty_review" in tickets_df.columns:

            warranty_count = len(
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

    negative_count = 0

    if not followups_df.empty:

        if "sentiment" in followups_df.columns:

            negative_count = len(
                followups_df[
                    followups_df[
                        "sentiment"
                    ]
                    == "Negative"
                ]
            )

    st.html(
        """
        <div class="section-title">
            AI Attention Needed
        </div>
        """
    )

    st.html(
        f"""
        <div class="alert alert-red">

            <b>
                {critical_cases} Critical Case(s)
            </b>

            <br>

            <span class="small">
                Immediate technician escalation recommended.
            </span>

        </div>
        """
    )

    st.html(
        f"""
        <div class="alert alert-orange">

            <b>
                {warranty_count} Warranty Review(s)
            </b>

            <br>

            <span class="small">
                Possible service-linked warranty issue.
            </span>

        </div>
        """
    )

    st.html(
        f"""
        <div class="alert alert-purple">

            <b>
                {negative_count} Negative Sentiment Case(s)
            </b>

            <br>

            <span class="small">
                Customer recovery action recommended.
            </span>

        </div>
        """
    )


st.write("")


st.html(
    """
    <div class="section-title">
        Recent AI Follow-ups
    </div>
    """
)


if (
    not followups_df.empty
    and not repairs_df.empty
):

    display_followups = (
        followups_df.merge(
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
    )

    wanted_columns = [
        "customer_name",
        "device",
        "repair_type",
        "call_status",
        "health_status",
        "risk_score",
        "recommended_action"
    ]

    available_columns = [
        col
        for col in wanted_columns
        if col in display_followups.columns
    ]

    display_followups = (
        display_followups[
            available_columns
        ].copy()
    )

    rename_map = {
        "customer_name": "Customer",
        "device": "Device",
        "repair_type": "Repair",
        "call_status": "Call Status",
        "health_status": "Health",
        "risk_score": "Risk Score",
        "recommended_action": "AI Action"
    }

    display_followups.rename(
        columns=rename_map,
        inplace=True
    )

    st.dataframe(
        display_followups,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No follow-up data available."
    )


st.write("")


issue_col, case_col = st.columns(
    [
        1.25,
        1
    ]
)


with issue_col:

    st.html(
        """
        <div class="section-title">
            Issue Breakdown
        </div>
        """
    )

    if (
        not followups_df.empty
        and not repairs_df.empty
    ):

        issue_df = followups_df[
            followups_df[
                "issue_detected"
            ]
            == "Yes"
        ].merge(
            repairs_df[
                [
                    "repair_id",
                    "repair_type"
                ]
            ],
            on="repair_id",
            how="left"
        )

        if not issue_df.empty:

            issue_summary = (
                issue_df.groupby(
                    "repair_type"
                )
                .size()
                .reset_index(
                    name="Issues"
                )
            )

            issue_fig = px.bar(
                issue_summary,
                x="repair_type",
                y="Issues"
            )

            issue_fig.update_layout(
                height=300,
                margin=dict(
                    l=5,
                    r=5,
                    t=5,
                    b=5
                ),
                paper_bgcolor="white",
                plot_bgcolor="white",
                xaxis_title="",
                yaxis_title="Issues",
                showlegend=False
            )

            st.plotly_chart(
                issue_fig,
                use_container_width=True
            )

        else:

            st.success(
                "No detected issues."
            )

    else:

        st.info(
            "No issue data available."
        )


with case_col:

    st.html(
        """
        <div class="section-title">
            Highest-Risk Case
        </div>
        """
    )

    if (
        not followups_df.empty
        and "risk_score"
        in followups_df.columns
    ):

        temp_df = followups_df.copy()

        temp_df["risk_score"] = (
            pd.to_numeric(
                temp_df["risk_score"],
                errors="coerce"
            )
            .fillna(0)
        )

        high_risk = (
            temp_df.sort_values(
                by="risk_score",
                ascending=False
            )
            .iloc[0]
        )

        repair_match = repairs_df[
            repairs_df[
                "repair_id"
            ].astype(str)
            == str(
                high_risk[
                    "repair_id"
                ]
            )
        ]

        if not repair_match.empty:

            repair_info = (
                repair_match.iloc[0]
            )

            device = repair_info.get(
                "device",
                "Unknown"
            )

            repair_type = repair_info.get(
                "repair_type",
                "Unknown"
            )

        else:

            device = "Unknown"
            repair_type = "Unknown"

        st.html(
            f"""
            <div class="panel">

                <div class="case-name">
                    {high_risk["customer_name"]}
                </div>

                <div class="small">
                    {device}
                    •
                    {repair_type}
                </div>

                <hr>

                <div class="small">
                    AI SERVICE RISK SCORE
                </div>

                <div class="case-risk">
                    {int(high_risk["risk_score"])}/100
                </div>

                <b>
                    Severity:
                </b>

                {high_risk["severity"]}

                <br>

                <b>
                    Sentiment:
                </b>

                {high_risk["sentiment"]}

                <br><br>

                <b>
                    Recommended Action
                </b>

                <br>

                <span class="small">
                    {high_risk["recommended_action"]}
                </span>

            </div>
            """
        )

    else:

        st.info(
            "No case data available."
        )


st.write("")


flow_col, recovery_col = st.columns(
    [
        1.2,
        1
    ]
)


with flow_col:

    st.html(
        """
        <div class="section-title">
            Autonomous Service Flow
        </div>
        """
    )

    st.html(
        """
        <div class="panel">

            <div class="flow-step">

                <div class="flow-num">
                    01
                </div>

                <div>

                    <div class="flow-title">
                        Service Completed
                    </div>

                    <div class="flow-sub">
                        Repair status changes to completed.
                    </div>

                </div>

            </div>

            <div class="flow-step">

                <div class="flow-num">
                    02
                </div>

                <div>

                    <div class="flow-title">
                        AI Follow-up Scheduled
                    </div>

                    <div class="flow-sub">
                        Timing is selected automatically by repair type.
                    </div>

                </div>

            </div>

            <div class="flow-step">

                <div class="flow-num">
                    03
                </div>

                <div>

                    <div class="flow-title">
                        CALL-E Conversation
                    </div>

                    <div class="flow-sub">
                        Customer is called and service health is verified.
                    </div>

                </div>

            </div>

            <div class="flow-step">

                <div class="flow-num">
                    04
                </div>

                <div>

                    <div class="flow-title">
                        AI Decision
                    </div>

                    <div class="flow-sub">
                        Healthy, issue or critical case classification.
                    </div>

                </div>

            </div>

            <div class="flow-step">

                <div class="flow-num">
                    05
                </div>

                <div>

                    <div class="flow-title">
                        Recovery Action
                    </div>

                    <div class="flow-sub">
                        Ticket, technician action and verification loop.
                    </div>

                </div>

            </div>

        </div>
        """
    )


with recovery_col:

    st.html(
        """
        <div class="section-title">
            Recovery Operations
        </div>
        """
    )

    r1, r2 = st.columns(
        2
    )

    with r1:

        st.metric(
            "Open Recovery Cases",
            open_recovery_cases
        )

    with r2:

        st.metric(
            "Resolved Cases",
            resolved_cases
        )

    st.write("")

    st.html(
        """
        <div class="ai-panel">

            <b>
                🧠 AI Recommendation
            </b>

            <br><br>

            <span class="small">
                Prioritize critical and reopened cases first.
                After technician work, verify the outcome with
                the customer before closing the case.
            </span>

        </div>
        """
    )


st.write("")


st.html(
    """
    <div class="section-title">
        Upcoming Autonomous Calls
    </div>
    """
)


if upcoming_followups_df.empty:

    st.info(
        "No upcoming AI follow-up calls."
    )

else:

    upcoming_columns = [
        "customer_name",
        "device",
        "repair_type",
        "completed_at",
        "followup_time"
    ]

    available_columns = [
        col
        for col in upcoming_columns
        if col
        in upcoming_followups_df.columns
    ]

    upcoming_display = (
        upcoming_followups_df[
            available_columns
        ].copy()
    )

    upcoming_display.rename(
        columns={
            "customer_name":
                "Customer",
            "device":
                "Device",
            "repair_type":
                "Repair",
            "completed_at":
                "Service Completed",
            "followup_time":
                "AI Follow-up Time"
        },
        inplace=True
    )

    st.dataframe(
        upcoming_display,
        use_container_width=True,
        hide_index=True
    )


st.write("")

st.caption(
    "AfterCare AI • Autonomous Post-Service Recovery Platform"
)