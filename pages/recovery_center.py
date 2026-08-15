import streamlit as st
import pandas as pd

from services.ui_fix import apply_html_fix

from services.resolution_service import (
    mark_resolution_in_progress,
    mark_resolution_completed,
    save_verification_result,
)

from services.verification_call_service import (
    make_live_verification_call,
)


apply_html_fix()


RESOLUTIONS_FILE = "data/resolutions.csv"
TICKETS_FILE = "data/tickets.csv"
REPAIRS_FILE = "data/repairs.csv"


# =========================================================
# PAGE HEADER
# =========================================================

st.title("🛠️ Service Recovery Center")

st.caption(
    "Technician recovery → Live CALL-E verification → "
    "Automatic closure or escalation"
)


# =========================================================
# LOAD DATA
# =========================================================

try:
    resolutions_df = pd.read_csv(
        RESOLUTIONS_FILE
    )
except Exception:
    resolutions_df = pd.DataFrame()


try:
    tickets_df = pd.read_csv(
        TICKETS_FILE
    )
except Exception:
    tickets_df = pd.DataFrame()


try:
    repairs_df = pd.read_csv(
        REPAIRS_FILE
    )
except Exception:
    repairs_df = pd.DataFrame()


# =========================================================
# NO RECOVERY CASES
# =========================================================

if resolutions_df.empty:

    st.info(
        "No recovery cases available yet."
    )

    st.stop()


# =========================================================
# METRICS
# =========================================================

total_cases = len(
    resolutions_df
)

scheduled = (
    resolutions_df["status"]
    .eq("Scheduled")
    .sum()
    if "status" in resolutions_df.columns
    else 0
)

in_progress = (
    resolutions_df["status"]
    .eq("In Progress")
    .sum()
    if "status" in resolutions_df.columns
    else 0
)

resolved = (
    resolutions_df["status"]
    .eq("Resolved")
    .sum()
    if "status" in resolutions_df.columns
    else 0
)

reopened = (
    resolutions_df["status"]
    .eq("Reopened")
    .sum()
    if "status" in resolutions_df.columns
    else 0
)


m1, m2, m3, m4, m5 = st.columns(
    5
)

m1.metric(
    "Recovery Cases",
    total_cases
)

m2.metric(
    "Scheduled",
    scheduled
)

m3.metric(
    "In Progress",
    in_progress
)

m4.metric(
    "Resolved",
    resolved
)

m5.metric(
    "Reopened",
    reopened
)


st.divider()


# =========================================================
# SELECT RECOVERY CASE
# =========================================================

if "resolution_id" not in resolutions_df.columns:

    st.error(
        "resolution_id column missing in resolutions.csv"
    )

    st.stop()


resolution_ids = (
    resolutions_df[
        "resolution_id"
    ]
    .dropna()
    .astype(str)
    .tolist()
)


if not resolution_ids:

    st.info(
        "No valid recovery case found."
    )

    st.stop()


selected_resolution = st.selectbox(
    "Select Recovery Case",
    resolution_ids
)


selected_rows = resolutions_df[
    resolutions_df[
        "resolution_id"
    ].astype(str)
    == str(
        selected_resolution
    )
]


if selected_rows.empty:

    st.error(
        "Selected recovery case not found."
    )

    st.stop()


case = (
    selected_rows
    .iloc[0]
    .to_dict()
)


ticket_id = str(
    case.get(
        "ticket_id",
        ""
    )
)


repair_id = str(
    case.get(
        "repair_id",
        ""
    )
)


# =========================================================
# FIND LINKED TICKET
# =========================================================

ticket = {}


if (
    not tickets_df.empty
    and "ticket_id" in tickets_df.columns
):

    matched_ticket = tickets_df[
        tickets_df[
            "ticket_id"
        ].astype(str)
        == ticket_id
    ]

    if not matched_ticket.empty:

        ticket = (
            matched_ticket
            .iloc[0]
            .to_dict()
        )


# =========================================================
# FIND LINKED REPAIR
# =========================================================

repair = {}


if (
    not repairs_df.empty
    and "repair_id" in repairs_df.columns
):

    matched_repair = repairs_df[
        repairs_df[
            "repair_id"
        ].astype(str)
        == repair_id
    ]

    if not matched_repair.empty:

        repair = (
            matched_repair
            .iloc[0]
            .to_dict()
        )


# =========================================================
# BUILD CASE DATA
# =========================================================

customer_name = (
    case.get("customer_name")
    or repair.get("customer_name")
    or "Customer"
)


phone = (
    repair.get(
        "phone",
        ""
    )
)


device = (
    repair.get(
        "device",
        "Device"
    )
)


repair_type = (
    repair.get(
        "repair_type",
        "Repair"
    )
)


issue = (
    ticket.get("issue")
    or "Reported post-service issue"
)


priority = (
    case.get("priority")
    or ticket.get("priority")
    or "P1"
)


assigned_to = (
    case.get("assigned_to")
    or ticket.get("assigned_team")
    or "Technician Team"
)


resolution_type = (
    case.get("resolution_type")
    or "Technician Revisit"
)


status = str(
    case.get(
        "status",
        "Scheduled"
    )
).strip()


# =========================================================
# CASE INTELLIGENCE
# =========================================================

st.subheader(
    "Recovery Case Intelligence"
)


left, right = st.columns(
    2
)


with left:

    st.write(
        f"**Customer:** {customer_name}"
    )

    st.write(
        f"**Device:** {device}"
    )

    st.write(
        f"**Repair:** {repair_type}"
    )

    st.write(
        f"**Original Issue:** {issue}"
    )


with right:

    st.write(
        f"**Recovery Case:** {selected_resolution}"
    )

    st.write(
        f"**Ticket:** {ticket_id}"
    )

    st.write(
        f"**Priority:** {priority}"
    )

    st.write(
        f"**Assigned To:** {assigned_to}"
    )


st.divider()


# =========================================================
# CURRENT STATUS
# =========================================================

st.subheader(
    "Current Recovery Status"
)


if status == "Scheduled":

    st.warning(
        "🟡 Recovery Scheduled"
    )


elif status == "In Progress":

    st.info(
        "🔧 Technician Recovery In Progress"
    )


elif status == "Resolved":

    st.success(
        "✅ Technician Work Completed"
    )


elif status == "Reopened":

    st.error(
        "🚨 Recovery Reopened"
    )


else:

    st.write(
        f"Status: {status}"
    )


# =========================================================
# SCHEDULED CASE
# =========================================================

if status == "Scheduled":

    st.write("")

    st.info(
        "Recovery case is ready to be assigned "
        "to the technician."
    )

    if st.button(
        "▶️ Start Recovery",
        type="primary",
        use_container_width=True
    ):

        try:

            mark_resolution_in_progress(
                selected_resolution
            )

            st.success(
                "Recovery started."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Could not start recovery: {e}"
            )


# =========================================================
# IN PROGRESS CASE
# =========================================================

elif status == "In Progress":

    st.write("")

    st.info(
        "Technician is currently working "
        "on the customer's reported issue."
    )

    if st.button(
        "✅ Mark Technician Work Complete",
        type="primary",
        use_container_width=True
    ):

        try:

            mark_resolution_completed(
                selected_resolution
            )

            st.success(
                "Technician work marked complete."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Could not complete recovery: {e}"
            )


# =========================================================
# REOPENED CASE
# =========================================================

elif status == "Reopened":

    st.write("")

    st.error(
        "Customer did not confirm the issue "
        "was resolved."
    )

    st.write(
        "The ticket has been escalated and "
        "another technician recovery is required."
    )

    if st.button(
        "🔄 Restart Technician Recovery",
        type="primary",
        use_container_width=True
    ):

        try:

            mark_resolution_in_progress(
                selected_resolution
            )

            st.success(
                "Recovery restarted."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Could not restart recovery: {e}"
            )


# =========================================================
# RESOLVED CASE
# LIVE SECOND CALL-E VERIFICATION
# =========================================================

elif status == "Resolved":

    st.divider()

    st.subheader(
        "📞 Live Customer Verification"
    )


    customer_confirmed_value = str(
        case.get(
            "customer_confirmed",
            ""
        )
    ).strip().lower()


    already_verified = (
        customer_confirmed_value
        in [
            "yes",
            "true",
            "no",
            "false"
        ]
    )


    # =====================================================
    # ALREADY VERIFIED
    # =====================================================

    if already_verified:

        if customer_confirmed_value in [
            "yes",
            "true"
        ]:

            st.success(
                "✅ Customer has already confirmed "
                "that the issue is resolved."
            )

        else:

            st.error(
                "🚨 Customer previously confirmed "
                "that the issue is still unresolved."
            )


        st.write(
            "**Customer Confirmed:**",
            case.get(
                "customer_confirmed",
                ""
            )
        )


        st.write(
            "**Final CSAT:**",
            case.get(
                "final_csat",
                ""
            )
        )


        st.write(
            "**Verification Feedback:**",
            case.get(
                "verification_feedback",
                ""
            )
        )


        st.write(
            "**Verification Call ID:**",
            case.get(
                "verification_call_id",
                ""
            )
        )


        st.write(
            "**Verified At:**",
            case.get(
                "verified_at",
                ""
            )
        )


    # =====================================================
    # NOT VERIFIED YET
    # =====================================================

    else:

        if not phone:

            st.error(
                "Customer phone number is missing "
                "for this repair."
            )

        else:

            st.success(
                "Technician work is complete. "
                "CALL-E can now call the customer "
                "to verify whether the issue is "
                "actually resolved."
            )


            st.write(
                f"**Customer:** {customer_name}"
            )

            st.write(
                f"**Phone:** {phone}"
            )

            st.write(
                f"**Original Issue:** {issue}"
            )

            st.write(
                f"**Recovery Action:** {resolution_type}"
            )


            verification_case = {

                "customer_name":
                    customer_name,

                "phone":
                    phone,

                "device":
                    device,

                "repair_type":
                    repair_type,

                "issue":
                    issue,

                "resolution_type":
                    resolution_type,

                "resolution_id":
                    selected_resolution,

                "ticket_id":
                    ticket_id,

                "repair_id":
                    repair_id
            }


            st.write("")


            if st.button(
                "📞 Run Live CALL-E Verification",
                type="primary",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        "CALL-E is calling the customer. "
                        "Please answer the call and "
                        "complete the verification..."
                    ):

                        result = (
                            make_live_verification_call(
                                verification_case
                            )
                        )


                    saved = (
                        save_verification_result(

                            resolution_id=
                                selected_resolution,

                            customer_confirmed=
                                result.get(
                                    "customer_confirmed",
                                    False
                                ),

                            final_csat=
                                result.get(
                                    "final_csat",
                                    3
                                ),

                            call_id=
                                result.get(
                                    "call_id",
                                    ""
                                ),

                            feedback=
                                result.get(
                                    "feedback",
                                    ""
                                )
                        )
                    )


                    # =====================================
                    # RESOLVED
                    # =====================================

                    if result.get(
                        "customer_confirmed",
                        False
                    ):

                        st.success(
                            "✅ Customer confirmed that "
                            "the issue is resolved."
                        )

                        st.success(
                            "Ticket automatically closed."
                        )

                        st.success(
                            "Customer health updated "
                            "to Healthy."
                        )


                    # =====================================
                    # NOT RESOLVED
                    # =====================================

                    else:

                        st.error(
                            "🚨 Customer confirmed that "
                            "the issue is still unresolved."
                        )

                        st.error(
                            "Recovery automatically reopened."
                        )

                        st.error(
                            "Ticket automatically escalated."
                        )


                    # =====================================
                    # RESULT
                    # =====================================

                    st.subheader(
                        "Verification Result"
                    )


                    st.json(
                        {
                            "Call ID":
                                result.get(
                                    "call_id"
                                ),

                            "Issue Resolved":
                                result.get(
                                    "issue_resolved"
                                ),

                            "Customer Confirmed":
                                result.get(
                                    "customer_confirmed"
                                ),

                            "Final CSAT":
                                result.get(
                                    "final_csat"
                                ),

                            "Feedback":
                                result.get(
                                    "feedback"
                                ),

                            "New Recovery Status":
                                saved.get(
                                    "status"
                                ),

                            "Ticket ID":
                                saved.get(
                                    "ticket_id"
                                )
                        }
                    )


                    # =====================================
                    # TRANSCRIPT
                    # =====================================

                    with st.expander(
                        "📄 CALL-E Verification Transcript"
                    ):

                        transcript = result.get(
                            "transcript",
                            []
                        )

                        if transcript:

                            for turn in transcript:

                                speaker = str(
                                    turn.get(
                                        "speaker",
                                        ""
                                    )
                                ).upper()

                                text = turn.get(
                                    "text",
                                    ""
                                )

                                st.write(
                                    f"**{speaker}:** {text}"
                                )

                        else:

                            st.write(
                                "No transcript available."
                            )


                    st.write("")


                    if st.button(
                        "🔄 Refresh Recovery Center"
                    ):

                        st.rerun()


                except Exception as e:

                    st.error(
                        f"Live verification call failed: {e}"
                    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AfterCare AI • Autonomous Closed-Loop "
    "Post-Service Recovery powered by CALL-E"
)