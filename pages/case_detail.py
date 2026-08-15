import streamlit as st
import pandas as pd
from services.ui_fix import apply_html_fix
apply_html_fix()

st.set_page_config(
    page_title="Case Intelligence | AfterCare AI",
    page_icon="🧠",
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
    repairs_df,
    on=[
        "repair_id",
        "customer_name"
    ],
    how="left"
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
    font-size: 28px;
    font-weight: 800;
    margin-top: 7px;
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

.risk-panel {
    background: #FEF3F2;
    border: 1px solid #FECDCA;
    border-radius: 18px;
    padding: 20px;
}

.success-panel {
    background: #ECFDF3;
    border: 1px solid #ABEFC6;
    border-radius: 18px;
    padding: 18px;
}

.section-title {
    font-size: 18px;
    font-weight: 750;
    color: var(--text);
    margin-bottom: 12px;
}

.label {
    color: var(--muted);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.04em;
}

.value {
    color: var(--text);
    font-size: 14px;
    font-weight: 650;
    margin-top: 3px;
}

.info-grid {
    display: grid;
    grid-template-columns:
        repeat(
            2,
            minmax(
                0,
                1fr
            )
        );
    gap: 14px;
    margin-top: 16px;
}

.info-box {
    background: #F9FAFB;
    border: 1px solid #F2F4F7;
    border-radius: 14px;
    padding: 13px;
}

.reason-item {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    padding: 11px 0;
    border-bottom: 1px solid #EAECF0;
}

.reason-icon {
    width: 24px;
    height: 24px;
    min-width: 24px;
    border-radius: 8px;
    background: #F4F3FF;
    color: #7F56D9;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
}

.reason-text {
    color: #475467;
    font-size: 13px;
    line-height: 1.5;
}

.risk-score {
    font-size: 46px;
    font-weight: 850;
    color: #D92D20;
    letter-spacing: -0.04em;
}

.risk-label {
    color: #667085;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
}

.timeline-item {
    display: flex;
    gap: 14px;
    padding-bottom: 16px;
}

.timeline-dot {
    width: 30px;
    height: 30px;
    min-width: 30px;
    border-radius: 10px;
    background: #F4F3FF;
    color: #7F56D9;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 11px;
    font-weight: 800;
}

.timeline-title {
    font-size: 13px;
    font-weight: 700;
    color: #101828;
}

.timeline-sub {
    font-size: 12px;
    color: #667085;
    margin-top: 2px;
}

.evidence-chip {
    display: inline-block;
    padding: 6px 9px;
    margin-right: 6px;
    margin-bottom: 6px;
    border-radius: 999px;
    background: #F2F4F7;
    color: #344054;
    font-size: 11px;
    font-weight: 650;
}

.small {
    color: var(--muted);
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="page-title">AI Case Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Understand what happened, why AI classified the case, and what action should happen next.'
    '</div>',
    unsafe_allow_html=True
)

customer_options = (
    merged_df[
        "customer_name"
    ]
    .dropna()
    .unique()
    .tolist()
)

selected_customer = st.selectbox(
    "Select Customer Case",
    customer_options
)

case = merged_df[
    merged_df[
        "customer_name"
    ] == selected_customer
].iloc[0]

repair_id = case[
    "repair_id"
]

ticket_match = tickets_df[
    tickets_df[
        "repair_id"
    ] == repair_id
]

if not ticket_match.empty:

    ticket = ticket_match.iloc[0]

    ticket_id = ticket[
        "ticket_id"
    ]

    ticket_status = ticket[
        "status"
    ]

    issue_text = ticket[
        "issue"
    ]

    assigned_team = ticket[
        "assigned_team"
    ]

    warranty_review = ticket[
        "warranty_review"
    ]

else:

    ticket = None

    ticket_id = "No Ticket"

    ticket_status = "Not Required"

    issue_text = (
        "Customer reported no post-service issue."
    )

    assigned_team = "None"

    warranty_review = "Not Required"

resolution_match = resolutions_df[
    resolutions_df[
        "ticket_id"
    ] == ticket_id
]

if not resolution_match.empty:

    resolution = resolution_match.iloc[0]

    resolution_id = resolution[
        "resolution_id"
    ]

    recovery_status = resolution[
        "status"
    ]

else:

    resolution = None

    resolution_id = "None"

    recovery_status = "Not Required"

risk_score = case[
    "risk_score"
]

severity = case[
    "severity"
]

sentiment = case[
    "sentiment"
]

health_status = case[
    "health_status"
]

action = case[
    "recommended_action"
]

call_status = case[
    "call_status"
]

m1, m2, m3, m4 = st.columns(4)

metric_data = [
    (
        "AI RISK SCORE",
        f"{risk_score}/100"
    ),
    (
        "SEVERITY",
        severity
    ),
    (
        "SENTIMENT",
        sentiment
    ),
    (
        "SERVICE HEALTH",
        health_status
    )
]

for column, metric in zip(
    [
        m1,
        m2,
        m3,
        m4
    ],
    metric_data
):

    with column:

        st.markdown(f"""
        <div class="metric-card">

            <div class="metric-label">
                {metric[0]}
            </div>

            <div class="metric-value">
                {metric[1]}
            </div>

        </div>
        """, unsafe_allow_html=True)

st.write("")

left, right = st.columns(
    [
        1.35,
        1
    ],
    gap="large"
)

with left:

    st.markdown(
        '<div class="section-title">Customer & Service Context</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="panel">

        <div style="
            font-size:20px;
            font-weight:750;
            color:#101828;
        ">
            {case["customer_name"]}
        </div>

        <div class="small">
            {case["device"]}
            •
            {case["repair_type"]}
        </div>

        <div class="info-grid">

            <div class="info-box">

                <div class="label">
                    REPAIR ID
                </div>

                <div class="value">
                    {repair_id}
                </div>

            </div>

            <div class="info-box">

                <div class="label">
                    CALL STATUS
                </div>

                <div class="value">
                    {call_status}
                </div>

            </div>

            <div class="info-box">

                <div class="label">
                    SERVICE COMPLETED
                </div>

                <div class="value">
                    {case["completed_at"]}
                </div>

            </div>

            <div class="info-box">

                <div class="label">
                    FOLLOW-UP TIME
                </div>

                <div class="value">
                    {case["scheduled_at"]}
                </div>

            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown(
        '<div class="section-title">🧠 AI Conversation Intelligence</div>',
        unsafe_allow_html=True
    )

    if health_status == "Healthy":

        ai_summary = (
            f"The customer confirmed that the {case['device']} "
            f"is functioning normally after the recent "
            f"{case['repair_type'].lower()}. "
            f"No post-service issue was detected and no recovery action is required."
        )

    else:

        ai_summary = (
            f"The post-service follow-up identified a potential problem "
            f"after {case['repair_type'].lower()} on the {case['device']}. "
            f"The case was classified as {severity.lower()} severity "
            f"with {sentiment.lower()} customer sentiment."
        )

    st.markdown(f"""
    <div class="ai-panel">

        <b>
            AI Case Summary
        </b>

        <br><br>

        <span style="
            color:#475467;
            font-size:13px;
            line-height:1.6;
        ">
            {ai_summary}
        </span>

        <br><br>

        <b>
            Detected Issue
        </b>

        <br><br>

        <span style="
            color:#475467;
            font-size:13px;
        ">
            {issue_text}
        </span>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown(
        '<div class="section-title">Why AI Made This Decision</div>',
        unsafe_allow_html=True
    )

    reasoning = []

    if health_status == "Healthy":

        reasoning.append(
            "Customer confirmed the repaired device is working normally."
        )

        reasoning.append(
            "No technical problem was reported during the follow-up."
        )

        reasoning.append(
            "No warranty or technician intervention is currently required."
        )

    else:

        reasoning.append(
            "Customer reported a problem after the repair was completed."
        )

        if severity in [
            "High",
            "Critical"
        ]:

            reasoning.append(
                f"The issue was classified as {severity.lower()} severity, increasing service recovery priority."
            )

        if sentiment == "Negative":

            reasoning.append(
                "Negative customer sentiment increases dissatisfaction and churn risk."
            )

        if warranty_review in [
            "Recommended",
            "Required"
        ]:

            reasoning.append(
                "The issue may be related to the recently repaired component, so warranty review is recommended."
            )

        if severity == "Critical":

            reasoning.append(
                "The case requires immediate human intervention because it was classified as critical."
            )

    reasoning_html = """
    <div class="panel">
    """

    for index, item in enumerate(
        reasoning,
        start=1
    ):

        reasoning_html += f"""
        <div class="reason-item">

            <div class="reason-icon">
                {index}
            </div>

            <div class="reason-text">
                {item}
            </div>

        </div>
        """

    reasoning_html += """
    </div>
    """

    st.markdown(
        reasoning_html,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        '<div class="section-title">Decision Evidence</div>',
        unsafe_allow_html=True
    )

    evidence = [
        f"Repair: {case['repair_type']}",
        f"Health: {health_status}",
        f"Severity: {severity}",
        f"Sentiment: {sentiment}",
        f"Risk: {risk_score}/100"
    ]

    if warranty_review != "Not Required":

        evidence.append(
            f"Warranty: {warranty_review}"
        )

    evidence_html = """
    <div class="panel">
    """

    for item in evidence:

        evidence_html += f"""
        <span class="evidence-chip">
            {item}
        </span>
        """

    evidence_html += """
    </div>
    """

    st.markdown(
        evidence_html,
        unsafe_allow_html=True
    )

with right:

    st.markdown(
        '<div class="section-title">AI Risk Assessment</div>',
        unsafe_allow_html=True
    )

    if risk_score >= 80:

        risk_level = "Critical"

    elif risk_score >= 60:

        risk_level = "High"

    elif risk_score >= 30:

        risk_level = "Medium"

    else:

        risk_level = "Low"

    st.markdown(f"""
    <div class="risk-panel">

        <div class="risk-label">
            SERVICE RISK SCORE
        </div>

        <div class="risk-score">
            {risk_score}
        </div>

        <span class="small">
            Risk Level:
            <b>
                {risk_level}
            </b>
        </span>

        <hr>

        <b>
            Severity
        </b>

        <br>

        <span class="small">
            {severity}
        </span>

        <br><br>

        <b>
            Customer Sentiment
        </b>

        <br>

        <span class="small">
            {sentiment}
        </span>

        <br><br>

        <b>
            Warranty Review
        </b>

        <br>

        <span class="small">
            {warranty_review}
        </span>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown(
        '<div class="section-title">Recommended Action</div>',
        unsafe_allow_html=True
    )

    if health_status == "Healthy":

        st.markdown("""
        <div class="success-panel">

            <b>
                ✅ Close Service Case
            </b>

            <br><br>

            <span class="small">
                Customer confirmed that the service is working normally.
                No technician or support intervention is required.
            </span>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div class="ai-panel">

            <b>
                🧠 {action}
            </b>

            <br><br>

            <span class="small">
                This recommendation is generated from service context,
                issue severity, sentiment and risk indicators.
            </span>

        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown(
        '<div class="section-title">Operational Handoff</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="panel">

        <div class="label">
            TICKET
        </div>

        <div class="value">
            {ticket_id}
        </div>

        <br>

        <div class="label">
            TICKET STATUS
        </div>

        <div class="value">
            {ticket_status}
        </div>

        <br>

        <div class="label">
            ASSIGNED TEAM
        </div>

        <div class="value">
            {assigned_team}
        </div>

        <br>

        <div class="label">
            RECOVERY CASE
        </div>

        <div class="value">
            {resolution_id}
        </div>

        <br>

        <div class="label">
            RECOVERY STATUS
        </div>

        <div class="value">
            {recovery_status}
        </div>

    </div>
    """, unsafe_allow_html=True)

st.write("")

st.markdown(
    '<div class="section-title">Autonomous Decision Timeline</div>',
    unsafe_allow_html=True
)

timeline_steps = [
    (
        "01",
        "Service Completed",
        f"{case['repair_type']} completed for {case['device']}."
    ),
    (
        "02",
        "Follow-up Scheduled",
        f"AI follow-up scheduled for {case['scheduled_at']}."
    ),
    (
        "03",
        "CALL-E Follow-up",
        f"Customer call status: {call_status}."
    )
]

if health_status == "Healthy":

    timeline_steps.extend(
        [
            (
                "04",
                "Service Verified",
                "Customer confirmed the device is working normally."
            ),
            (
                "05",
                "Case Closed",
                "No ticket or service recovery required."
            )
        ]
    )

else:

    timeline_steps.extend(
        [
            (
                "04",
                "Issue Detected",
                issue_text
            ),
            (
                "05",
                "Risk Classified",
                f"{risk_level} risk • {risk_score}/100."
            ),
            (
                "06",
                "Ticket Created",
                f"{ticket_id} routed to {assigned_team}."
            ),
            (
                "07",
                "Recovery Started",
                f"{resolution_id} • {recovery_status}."
            )
        ]
    )

timeline_html = """
<div class="panel">
"""

for number, title, description in timeline_steps:

    timeline_html += f"""
    <div class="timeline-item">

        <div class="timeline-dot">
            {number}
        </div>

        <div>

            <div class="timeline-title">
                {title}
            </div>

            <div class="timeline-sub">
                {description}
            </div>

        </div>

    </div>
    """

timeline_html += """
</div>
"""

st.markdown(
    timeline_html,
    unsafe_allow_html=True
)

st.write("")

st.caption(
    "AfterCare AI • Explainable Autonomous Service Recovery"
)