import streamlit as st
import pandas as pd
from services.ui_fix import apply_html_fix
apply_html_fix()

from datetime import datetime

from services.scheduler import calculate_followup_time

st.set_page_config(
    page_title="New Service | AfterCare AI",
    page_icon="➕",
    layout="wide"
)

REPAIRS_FILE = "data/repairs.csv"
FOLLOWUPS_FILE = "data/followups.csv"
CUSTOMERS_FILE = "data/customers.csv"

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
}

.stApp {
    background: var(--bg);
}

.block-container {
    max-width: 1400px;
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
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 22px;
    box-shadow:
        0 6px 24px
        rgba(
            16,
            24,
            40,
            0.05
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
    border-radius: 20px;
    padding: 22px;
}

.section-title {
    font-size: 17px;
    font-weight: 750;
    color: var(--text);
    margin-bottom: 14px;
}

.label {
    color: var(--muted);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
}

.value {
    color: var(--text);
    font-size: 16px;
    font-weight: 700;
    margin-top: 3px;
}

.flow-step {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 15px;
}

.flow-number {
    width: 30px;
    height: 30px;
    border-radius: 10px;
    background: #F4F3FF;
    color: #7F56D9;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 800;
    flex-shrink: 0;
}

.flow-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
}

.flow-sub {
    color: var(--muted);
    font-size: 12px;
    margin-top: 2px;
}

.success-card {
    background: var(--green-soft);
    border: 1px solid #ABEFC6;
    border-radius: 18px;
    padding: 20px;
    margin-top: 18px;
}

.badge {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 999px;
    background: #ECFDF3;
    color: #027A48;
    font-size: 11px;
    font-weight: 700;
}

div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stDateInput"] input,
div[data-testid="stTimeInput"] input {
    border-radius: 12px !important;
}

button[kind="primary"] {
    border-radius: 12px !important;
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="page-title">Create Completed Service</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Add a completed repair and let AfterCare AI automatically schedule the post-service follow-up.'
    '</div>',
    unsafe_allow_html=True
)

left, right = st.columns(
    [1.25, 1],
    gap="large"
)

with left:

    st.markdown(
        '<div class="section-title">Customer & Service Information</div>',
        unsafe_allow_html=True
    )

    customer_name = st.text_input(
        "Customer Name",
        value="Demo Customer"
    )

    c1, c2 = st.columns(2)

    with c1:
        phone = st.text_input(
            "Phone Number",
            value="+919876543299"
        )

    with c2:
        email = st.text_input(
            "Email",
            value="demo@example.com"
        )

    device = st.selectbox(
        "Device",
        [
            "iPhone 15",
            "iPhone 14",
            "Samsung S24",
            "Samsung S23",
            "OnePlus 12",
            "OnePlus 11",
            "Pixel 8",
            "Xiaomi 14"
        ]
    )

    repair_type = st.selectbox(
        "Repair Type",
        [
            "Screen Replacement",
            "Display Repair",
            "Battery Replacement",
            "Charging Port Repair",
            "Camera Repair",
            "Water Damage Repair",
            "Other Repair"
        ]
    )

    d1, d2 = st.columns(2)

    with d1:
        completed_date = st.date_input(
            "Service Completion Date",
            value=datetime.now().date()
        )

    with d2:
        completed_time = st.time_input(
            "Service Completion Time",
            value=datetime.now().time().replace(
                second=0,
                microsecond=0
            )
        )

    service_status = "Completed"

with right:

    completed_at_preview = datetime.combine(
        completed_date,
        completed_time
    )

    followup_preview = calculate_followup_time(
        completed_at_preview,
        repair_type
    )

    st.markdown(
        '<div class="section-title">AI Automation Preview</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="ai-panel">

        <span class="badge">
            ⚡ AUTOMATION READY
        </span>

        <br><br>

        <div class="label">
            CUSTOMER
        </div>

        <div class="value">
            {customer_name}
        </div>

        <br>

        <div class="label">
            DEVICE
        </div>

        <div class="value">
            {device}
        </div>

        <br>

        <div class="label">
            REPAIR TYPE
        </div>

        <div class="value">
            {repair_type}
        </div>

        <br>

        <div class="label">
            SERVICE COMPLETED
        </div>

        <div class="value">
            {completed_at_preview.strftime("%d %b %Y • %I:%M %p")}
        </div>

        <br>

        <div class="label">
            AI FOLLOW-UP SCHEDULED
        </div>

        <div class="value">
            {followup_preview.strftime("%d %b %Y • %I:%M %p")}
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown(
        '<div class="section-title">What Happens Next</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="panel">

        <div class="flow-step">

            <div class="flow-number">
                01
            </div>

            <div>

                <div class="flow-title">
                    Service Event Captured
                </div>

                <div class="flow-sub">
                    Completed repair enters the automation engine.
                </div>

            </div>

        </div>

        <div class="flow-step">

            <div class="flow-number">
                02
            </div>

            <div>

                <div class="flow-title">
                    Smart Follow-up Scheduled
                </div>

                <div class="flow-sub">
                    Delay is selected automatically from repair type.
                </div>

            </div>

        </div>

        <div class="flow-step">

            <div class="flow-number">
                03
            </div>

            <div>

                <div class="flow-title">
                    CALL-E Calls Customer
                </div>

                <div class="flow-sub">
                    AI checks if the repaired device is working normally.
                </div>

            </div>

        </div>

        <div class="flow-step">

            <div class="flow-number">
                04
            </div>

            <div>

                <div class="flow-title">
                    AI Makes Decision
                </div>

                <div class="flow-sub">
                    Healthy, issue or critical case is identified.
                </div>

            </div>

        </div>

        <div class="flow-step">

            <div class="flow-number">
                05
            </div>

            <div>

                <div class="flow-title">
                    Recovery Starts Automatically
                </div>

                <div class="flow-sub">
                    Ticket and technician recovery workflow are created when required.
                </div>

            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

st.write("")

if st.button(
    "➕ Create Service & Activate AI Follow-up",
    type="primary",
    use_container_width=True
):

    if not customer_name.strip():
        st.error(
            "Customer name is required."
        )
        st.stop()

    if not phone.strip():
        st.error(
            "Phone number is required."
        )
        st.stop()

    repairs_df = pd.read_csv(
        REPAIRS_FILE
    )

    followups_df = pd.read_csv(
        FOLLOWUPS_FILE
    )

    customers_df = pd.read_csv(
        CUSTOMERS_FILE
    )

    repair_ids = (
        repairs_df["repair_id"]
        .astype(str)
        .str.extract(r"(\d+)")[0]
        .dropna()
        .astype(int)
    )

    if repair_ids.empty:
        next_repair_number = 1
    else:
        next_repair_number = (
            repair_ids.max() + 1
        )

    repair_id = (
        f"R{next_repair_number:03d}"
    )

    followup_ids = (
        followups_df["followup_id"]
        .astype(str)
        .str.extract(r"(\d+)")[0]
        .dropna()
        .astype(int)
    )

    if followup_ids.empty:
        next_followup_number = 1
    else:
        next_followup_number = (
            followup_ids.max() + 1
        )

    followup_id = (
        f"F{next_followup_number:03d}"
    )

    completed_at = datetime.combine(
        completed_date,
        completed_time
    )

    followup_time = calculate_followup_time(
        completed_at,
        repair_type
    )

    new_repair = {
        "repair_id": repair_id,
        "customer_name": customer_name,
        "phone": phone,
        "device": device,
        "repair_type": repair_type,
        "completed_at": completed_at.strftime(
            "%Y-%m-%d %H:%M"
        ),
        "status": service_status,
        "followup_time": followup_time.strftime(
            "%Y-%m-%d %H:%M"
        )
    }

    repairs_df = pd.concat(
        [
            repairs_df,
            pd.DataFrame(
                [new_repair]
            )
        ],
        ignore_index=True
    )

    repairs_df.to_csv(
        REPAIRS_FILE,
        index=False
    )

    new_followup = {
        "followup_id": followup_id,
        "repair_id": repair_id,
        "customer_name": customer_name,
        "scheduled_at": followup_time.strftime(
            "%Y-%m-%d %H:%M"
        ),
        "call_status": "Scheduled",
        "health_status": "Pending",
        "risk_score": 0,
        "issue_detected": "No",
        "severity": "Low",
        "sentiment": "Neutral",
        "recommended_action": "AI Follow-up Scheduled",
        "ticket_required": "No"
    }

    followups_df = pd.concat(
        [
            followups_df,
            pd.DataFrame(
                [new_followup]
            )
        ],
        ignore_index=True
    )

    followups_df.to_csv(
        FOLLOWUPS_FILE,
        index=False
    )

    existing_customer = customers_df[
        customers_df[
            "phone"
        ].astype(str) == str(phone)
    ]

    if existing_customer.empty:

        customer_ids = (
            customers_df["customer_id"]
            .astype(str)
            .str.extract(r"(\d+)")[0]
            .dropna()
            .astype(int)
        )

        if customer_ids.empty:
            next_customer_number = 1
        else:
            next_customer_number = (
                customer_ids.max() + 1
            )

        customer_id = (
            f"C{next_customer_number:03d}"
        )

        new_customer = {
            "customer_id": customer_id,
            "customer_name": customer_name,
            "phone": phone,
            "email": email,
            "total_repairs": 1,
            "last_device": device,
            "last_repair_type": repair_type,
            "last_service_date": completed_at.strftime(
                "%Y-%m-%d"
            ),
            "customer_status": "Pending Follow-up"
        }

        customers_df = pd.concat(
            [
                customers_df,
                pd.DataFrame(
                    [new_customer]
                )
            ],
            ignore_index=True
        )

    else:

        mask = (
            customers_df[
                "phone"
            ].astype(str)
            == str(phone)
        )

        customers_df.loc[
            mask,
            "customer_name"
        ] = customer_name

        customers_df.loc[
            mask,
            "email"
        ] = email

        customers_df.loc[
            mask,
            "total_repairs"
        ] = (
            customers_df.loc[
                mask,
                "total_repairs"
            ].astype(int)
            + 1
        )

        customers_df.loc[
            mask,
            "last_device"
        ] = device

        customers_df.loc[
            mask,
            "last_repair_type"
        ] = repair_type

        customers_df.loc[
            mask,
            "last_service_date"
        ] = completed_at.strftime(
            "%Y-%m-%d"
        )

        customers_df.loc[
            mask,
            "customer_status"
        ] = "Pending Follow-up"

    customers_df.to_csv(
        CUSTOMERS_FILE,
        index=False
    )

    st.markdown(f"""
    <div class="success-card">

        <b style="
            font-size:17px;
            color:#027A48;
        ">
            ✅ Service Activated Successfully
        </b>

        <br><br>

        Repair ID:
        <b>{repair_id}</b>

        <br>

        Follow-up ID:
        <b>{followup_id}</b>

        <br>

        Customer:
        <b>{customer_name}</b>

        <br>

        Device:
        <b>{device}</b>

        <br>

        Repair:
        <b>{repair_type}</b>

        <br><br>

        📞 AI follow-up scheduled for:

        <br>

        <b>
            {followup_time.strftime("%d %b %Y • %I:%M %p")}
        </b>

    </div>
    """, unsafe_allow_html=True)

    st.balloons()

st.write("")

st.caption(
    "AfterCare AI • Event-Driven Post-Service Automation"
)