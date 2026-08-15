import streamlit as st
import pandas as pd
from services.ui_fix import apply_html_fix
apply_html_fix()

st.set_page_config(
    page_title="Settings | AfterCare AI",
    page_icon="⚙️",
    layout="wide"
)

REPAIRS_FILE = "data/repairs.csv"
FOLLOWUPS_FILE = "data/followups.csv"
TICKETS_FILE = "data/tickets.csv"
CUSTOMERS_FILE = "data/customers.csv"
RESOLUTIONS_FILE = "data/resolutions.csv"

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
    max-width: 1350px;
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

.panel {
    background: white;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 22px;
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

.warning-panel {
    background: var(--orange-soft);
    border: 1px solid #FEDF89;
    border-radius: 18px;
    padding: 18px;
}

.danger-panel {
    background: var(--red-soft);
    border: 1px solid #FECDCA;
    border-radius: 18px;
    padding: 18px;
}

.success-panel {
    background: var(--green-soft);
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

.small {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.6;
}

.setting-title {
    color: var(--text);
    font-size: 14px;
    font-weight: 750;
}

.setting-sub {
    color: var(--muted);
    font-size: 12px;
    margin-top: 3px;
}

.badge {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
}

.badge-demo {
    background: var(--orange-soft);
    color: #B54708;
}

.badge-ready {
    background: var(--green-soft);
    color: #027A48;
}

button[kind="primary"] {
    border-radius: 12px !important;
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="page-title">Automation Settings</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Configure post-service automation behavior, AI risk rules and demo controls.'
    '</div>',
    unsafe_allow_html=True
)

left, right = st.columns(
    [1.2, 1],
    gap="large"
)

with left:

    st.markdown(
        '<div class="section-title">Follow-up Automation</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="panel">

        <div class="setting-title">
            Automatic Follow-up Calls
        </div>

        <div class="setting-sub">
            Schedule customer health checks automatically after a completed repair.
        </div>

    </div>
    """, unsafe_allow_html=True)

    automation_enabled = st.toggle(
        "Enable automatic follow-up workflow",
        value=True
    )

    st.write("")

    screen_delay = st.number_input(
        "Screen / Display Follow-up Delay (hours)",
        min_value=1,
        max_value=72,
        value=4
    )

    battery_delay = st.number_input(
        "Battery Follow-up Delay (hours)",
        min_value=1,
        max_value=72,
        value=8
    )

    charging_delay = st.number_input(
        "Charging Port Follow-up Delay (hours)",
        min_value=1,
        max_value=72,
        value=6
    )

    water_delay = st.number_input(
        "Water Damage Follow-up Delay (hours)",
        min_value=1,
        max_value=120,
        value=24
    )

    st.write("")

    st.markdown(
        '<div class="section-title">AI Risk Thresholds</div>',
        unsafe_allow_html=True
    )

    medium_threshold = st.slider(
        "Medium Risk Threshold",
        min_value=10,
        max_value=60,
        value=30
    )

    high_threshold = st.slider(
        "High Risk Threshold",
        min_value=40,
        max_value=85,
        value=60
    )

    critical_threshold = st.slider(
        "Critical Risk Threshold",
        min_value=60,
        max_value=100,
        value=80
    )

with right:

    st.markdown(
        '<div class="section-title">AI Operating Mode</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="ai-panel">

        <span class="
            badge
            badge-demo
        ">
            DEMO MODE
        </span>

        <br><br>

        <b>
            CALL-E Simulation Enabled
        </b>

        <br><br>

        <span class="small">
            Customer call outcomes are currently simulated
            so the complete recovery workflow can be tested
            without consuming a real voice API.
        </span>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    simulation_mode = st.toggle(
        "Use simulated AI calls",
        value=True
    )

    auto_ticket = st.toggle(
        "Automatically create tickets",
        value=True
    )

    auto_recovery = st.toggle(
        "Automatically create recovery cases",
        value=True
    )

    warranty_review = st.toggle(
        "Enable warranty-risk detection",
        value=True
    )

    safety_escalation = st.toggle(
        "Immediate escalation for safety issues",
        value=True
    )

    st.write("")

    st.markdown(
        '<div class="section-title">Automation Guardrails</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="warning-panel">

        <b>
            🛡️ Human-in-the-loop Guardrails
        </b>

        <br><br>

        <span class="small">

            • AI does not approve refunds automatically.

            <br>

            • AI does not guarantee warranty eligibility.

            <br>

            • Critical safety cases should be escalated to a human.

            <br>

            • Technician completion must be verified with the customer.

        </span>

    </div>
    """, unsafe_allow_html=True)

st.write("")

st.markdown(
    '<div class="section-title">Current Automation Policy</div>',
    unsafe_allow_html=True
)

p1, p2, p3 = st.columns(3)

with p1:

    st.markdown(f"""
    <div class="panel">

        <div class="setting-title">
            Follow-up Engine
        </div>

        <br>

        <span class="badge badge-ready">
            {
                "ACTIVE"
                if automation_enabled
                else "DISABLED"
            }
        </span>

        <br><br>

        <span class="small">
            Screen:
            <b>{screen_delay}h</b>

            <br>

            Battery:
            <b>{battery_delay}h</b>

            <br>

            Charging:
            <b>{charging_delay}h</b>

            <br>

            Water Damage:
            <b>{water_delay}h</b>
        </span>

    </div>
    """, unsafe_allow_html=True)

with p2:

    st.markdown(f"""
    <div class="panel">

        <div class="setting-title">
            Risk Policy
        </div>

        <br>

        <span class="small">

            Medium:
            <b>{medium_threshold}+</b>

            <br>

            High:
            <b>{high_threshold}+</b>

            <br>

            Critical:
            <b>{critical_threshold}+</b>

            <br><br>

            Critical cases should trigger
            immediate human escalation.

        </span>

    </div>
    """, unsafe_allow_html=True)

with p3:

    st.markdown(f"""
    <div class="panel">

        <div class="setting-title">
            Autonomous Actions
        </div>

        <br>

        <span class="small">

            Auto Ticket:
            <b>
                {"On" if auto_ticket else "Off"}
            </b>

            <br>

            Auto Recovery:
            <b>
                {"On" if auto_recovery else "Off"}
            </b>

            <br>

            Warranty Detection:
            <b>
                {"On" if warranty_review else "Off"}
            </b>

            <br>

            Safety Escalation:
            <b>
                {"On" if safety_escalation else "Off"}
            </b>

        </span>

    </div>
    """, unsafe_allow_html=True)

st.write("")

st.markdown(
    '<div class="section-title">Reset Hackathon Demo</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="danger-panel">

    <b>
        ⚠️ Reset Demo Dataset
    </b>

    <br><br>

    <span class="small">
        This will restore follow-ups, tickets and recovery cases
        to the original demo state. Use this before recording
        or presenting the complete product flow.
    </span>

</div>
""", unsafe_allow_html=True)

confirm_reset = st.checkbox(
    "I understand that current demo changes will be replaced."
)

if st.button(
    "Reset Demo Data",
    type="primary",
    use_container_width=True,
    disabled=not confirm_reset
):

    followups_reset = pd.DataFrame([
        {
            "followup_id": "F001",
            "repair_id": "R001",
            "customer_name": "Rahul Sharma",
            "scheduled_at": "2026-08-14 17:00",
            "call_status": "Completed",
            "health_status": "Issue Detected",
            "risk_score": 84,
            "issue_detected": "Yes",
            "severity": "High",
            "sentiment": "Negative",
            "recommended_action": "Technician Revisit",
            "ticket_required": "Yes"
        },
        {
            "followup_id": "F002",
            "repair_id": "R002",
            "customer_name": "Aisha Khan",
            "scheduled_at": "2026-08-14 19:15",
            "call_status": "Scheduled",
            "health_status": "Pending",
            "risk_score": 32,
            "issue_detected": "No",
            "severity": "Low",
            "sentiment": "Neutral",
            "recommended_action": "AI Follow-up Scheduled",
            "ticket_required": "No"
        },
        {
            "followup_id": "F003",
            "repair_id": "R003",
            "customer_name": "Vikram Patel",
            "scheduled_at": "2026-08-14 15:30",
            "call_status": "Completed",
            "health_status": "Healthy",
            "risk_score": 15,
            "issue_detected": "No",
            "severity": "Low",
            "sentiment": "Positive",
            "recommended_action": "Close Case",
            "ticket_required": "No"
        },
        {
            "followup_id": "F004",
            "repair_id": "R004",
            "customer_name": "Neha Verma",
            "scheduled_at": "2026-08-14 12:45",
            "call_status": "Completed",
            "health_status": "Healthy",
            "risk_score": 12,
            "issue_detected": "No",
            "severity": "Low",
            "sentiment": "Positive",
            "recommended_action": "Close Case",
            "ticket_required": "No"
        },
        {
            "followup_id": "F005",
            "repair_id": "R005",
            "customer_name": "Arjun Mehta",
            "scheduled_at": "2026-08-14 11:20",
            "call_status": "Completed",
            "health_status": "Critical",
            "risk_score": 93,
            "issue_detected": "Yes",
            "severity": "Critical",
            "sentiment": "Negative",
            "recommended_action": "Immediate Escalation",
            "ticket_required": "Yes"
        }
    ])

    tickets_reset = pd.DataFrame([
        {
            "ticket_id": "T001",
            "repair_id": "R001",
            "customer_name": "Rahul Sharma",
            "issue": "Touch freezing after screen replacement",
            "severity": "High",
            "priority": "P1",
            "status": "Open",
            "assigned_team": "Technician Team",
            "warranty_review": "Recommended",
            "created_at": "2026-08-14 17:08"
        },
        {
            "ticket_id": "T002",
            "repair_id": "R005",
            "customer_name": "Arjun Mehta",
            "issue": "Display issue with device heating",
            "severity": "Critical",
            "priority": "P0",
            "status": "Escalated",
            "assigned_team": "Senior Technician",
            "warranty_review": "Required",
            "created_at": "2026-08-14 11:28"
        }
    ])

    resolutions_reset = pd.DataFrame([
        {
            "resolution_id": "RS001",
            "ticket_id": "T001",
            "customer_name": "Rahul Sharma",
            "resolution_type": "Technician Revisit",
            "status": "Scheduled",
            "assigned_to": "Technician Team",
            "scheduled_for": "2026-08-15 10:00",
            "resolved_at": "",
            "customer_confirmed": "No",
            "final_csat": ""
        },
        {
            "resolution_id": "RS002",
            "ticket_id": "T002",
            "customer_name": "Arjun Mehta",
            "resolution_type": "Immediate Technician Escalation",
            "status": "In Progress",
            "assigned_to": "Senior Technician",
            "scheduled_for": "2026-08-14 18:00",
            "resolved_at": "",
            "customer_confirmed": "No",
            "final_csat": ""
        }
    ])

    followups_reset.to_csv(
        FOLLOWUPS_FILE,
        index=False
    )

    tickets_reset.to_csv(
        TICKETS_FILE,
        index=False
    )

    resolutions_reset.to_csv(
        RESOLUTIONS_FILE,
        index=False
    )

    st.success(
        "✅ Demo data restored successfully."
    )

    st.balloons()

st.write("")

st.caption(
    "AfterCare AI • Automation, Risk & Guardrail Configuration"
)