import streamlit as st
import pandas as pd
from services.ui_fix import apply_html_fix

apply_html_fix()

st.set_page_config(
    page_title="Tickets | AfterCare AI",
    page_icon="🎫",
    layout="wide"
)

TICKETS_FILE = "data/tickets.csv"
RESOLUTIONS_FILE = "data/resolutions.csv"

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

.ticket-card {
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

.ticket-title {
    font-size: 18px;
    font-weight: 750;
    color: var(--text);
}

.ticket-sub {
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
    margin-right: 6px;
}

.badge-p0 {
    background: var(--red-soft);
    color: #B42318;
}

.badge-p1 {
    background: var(--orange-soft);
    color: #B54708;
}

.badge-p2 {
    background: var(--blue-soft);
    color: #175CD3;
}

.badge-p3 {
    background: var(--green-soft);
    color: #027A48;
}

.badge-open {
    background: #FFF4E5;
    color: #B54708;
}

.badge-escalated {
    background: var(--red-soft);
    color: #B42318;
}

.badge-resolved {
    background: var(--green-soft);
    color: #027A48;
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
    '<div class="page-title">Service Recovery Tickets</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'AI-generated service cases that need technician, warranty or support intervention.'
    '</div>',
    unsafe_allow_html=True
)

total_tickets = len(tickets_df)

open_tickets = len(
    tickets_df[
        tickets_df["status"] == "Open"
    ]
)

escalated_tickets = len(
    tickets_df[
        tickets_df["status"] == "Escalated"
    ]
)

critical_tickets = len(
    tickets_df[
        tickets_df["priority"] == "P0"
    ]
)

recovery_linked = len(
    tickets_df[
        tickets_df["ticket_id"].isin(
            resolutions_df["ticket_id"]
        )
    ]
)

m1, m2, m3, m4, m5 = st.columns(5)

metrics = [
    ("TOTAL TICKETS", total_tickets),
    ("OPEN", open_tickets),
    ("ESCALATED", escalated_tickets),
    ("CRITICAL P0", critical_tickets),
    ("RECOVERY LINKED", recovery_linked)
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

    status_filter = st.selectbox(
        "Filter by Status",
        [
            "All",
            "Open",
            "Escalated",
            "Resolved"
        ]
    )

with filter_col2:

    priority_filter = st.selectbox(
        "Filter by Priority",
        [
            "All",
            "P0",
            "P1",
            "P2",
            "P3"
        ]
    )

filtered_df = tickets_df.copy()

if status_filter != "All":

    filtered_df = filtered_df[
        filtered_df[
            "status"
        ] == status_filter
    ]

if priority_filter != "All":

    filtered_df = filtered_df[
        filtered_df[
            "priority"
        ] == priority_filter
    ]

st.write("")

st.markdown(
    '<div class="section-title">Active Service Cases</div>',
    unsafe_allow_html=True
)

if filtered_df.empty:

    st.info(
        "No tickets match the selected filters."
    )

else:

    for _, row in filtered_df.iterrows():

        priority_class = {
            "P0": "badge-p0",
            "P1": "badge-p1",
            "P2": "badge-p2",
            "P3": "badge-p3"
        }.get(
            row["priority"],
            "badge-p3"
        )

        status_class = {
            "Open": "badge-open",
            "Escalated": "badge-escalated",
            "Resolved": "badge-resolved"
        }.get(
            row["status"],
            "badge-open"
        )

        recovery_match = resolutions_df[
            resolutions_df[
                "ticket_id"
            ] == row[
                "ticket_id"
            ]
        ]

        if not recovery_match.empty:

            recovery_id = recovery_match.iloc[0][
                "resolution_id"
            ]

            recovery_status = recovery_match.iloc[0][
                "status"
            ]

        else:

            recovery_id = "Not Created"
            recovery_status = "Pending"

        st.markdown(f"""
        <div class="ticket-card">

            <span class="
                badge
                {priority_class}
            ">
                {row["priority"]}
            </span>

            <span class="
                badge
                {status_class}
            ">
                {row["status"]}
            </span>

            <br><br>

            <div class="ticket-title">
                {row["ticket_id"]}
                •
                {row["customer_name"]}
            </div>

            <div class="ticket-sub">
                Repair Case:
                {row["repair_id"]}
            </div>

            <div class="info-grid">

                <div class="info-box">

                    <div class="info-label">
                        ISSUE
                    </div>

                    <div class="info-value">
                        {row["issue"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        SEVERITY
                    </div>

                    <div class="info-value">
                        {row["severity"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        ASSIGNED TEAM
                    </div>

                    <div class="info-value">
                        {row["assigned_team"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        WARRANTY REVIEW
                    </div>

                    <div class="info-value">
                        {row["warranty_review"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        CREATED AT
                    </div>

                    <div class="info-value">
                        {row["created_at"]}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        RECOVERY CASE
                    </div>

                    <div class="info-value">
                        {recovery_id}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        RECOVERY STATUS
                    </div>

                    <div class="info-value">
                        {recovery_status}
                    </div>

                </div>

                <div class="info-box">

                    <div class="info-label">
                        NEXT ACTION
                    </div>

                    <div class="info-value">
                        {
                            "Immediate escalation"
                            if row["priority"] == "P0"
                            else
                            "Technician follow-up"
                        }
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
        '<div class="section-title">Ticket Operations</div>',
        unsafe_allow_html=True
    )

    ticket_summary = (
        tickets_df[
            "status"
        ]
        .value_counts()
        .reset_index()
    )

    ticket_summary.columns = [
        "Status",
        "Tickets"
    ]

    st.dataframe(
        ticket_summary,
        use_container_width=True,
        hide_index=True
    )

with right:

    st.markdown(
        '<div class="section-title">🧠 AI Operations Recommendation</div>',
        unsafe_allow_html=True
    )

    if critical_tickets > 0:

        recommendation = (
            f"{critical_tickets} critical P0 case(s) require immediate "
            f"human or senior technician intervention. Prioritize these "
            f"before standard warranty or revisit cases."
        )

    elif escalated_tickets > 0:

        recommendation = (
            f"{escalated_tickets} escalated case(s) are active. "
            f"Ensure recovery ownership is assigned and verification "
            f"calls happen after technician completion."
        )

    else:

        recommendation = (
            "No critical ticket backlog detected. Continue monitoring "
            "open tickets and ensure every service recovery is verified "
            "with the customer before closure."
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
    '<div class="section-title">All Ticket Data</div>',
    unsafe_allow_html=True
)

st.dataframe(
    tickets_df,
    use_container_width=True,
    hide_index=True
)

st.write("")

st.caption(
    "AfterCare AI • Autonomous Ticket & Recovery Operations"
)