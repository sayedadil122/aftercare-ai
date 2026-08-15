import streamlit as st
import pandas as pd

from services.ui_fix import apply_html_fix
from services.calle_service import make_followup_call
from services.ai_analysis import analyze_call_result
from services.risk_engine import calculate_risk_score
from services.ticket_service import create_ticket
from services.resolution_service import create_recovery_case
from services.customer_service import update_customer_health


apply_html_fix()


FOLLOWUPS_FILE = "data/followups.csv"
REPAIRS_FILE = "data/repairs.csv"


def safe_read_csv(path):
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def save_followups(df):
    df.to_csv(
        FOLLOWUPS_FILE,
        index=False
    )


def prepare_text_column(
    df,
    column
):
    if column not in df.columns:
        df[column] = ""

    df[column] = df[column].astype("object")

    return df


followups_df = safe_read_csv(
    FOLLOWUPS_FILE
)

repairs_df = safe_read_csv(
    REPAIRS_FILE
)


st.title(
    "📞 Follow-up Calls"
)

st.caption(
    "AI-powered post-service health verification using CALL-E"
)


if followups_df.empty:
    st.info(
        "No follow-up calls available."
    )
    st.stop()


if repairs_df.empty:
    st.error(
        "No repair data found."
    )
    st.stop()


if "repair_id" not in followups_df.columns:
    st.error(
        "repair_id column missing in followups.csv"
    )
    st.stop()


if "repair_id" not in repairs_df.columns:
    st.error(
        "repair_id column missing in repairs.csv"
    )
    st.stop()


merged_df = followups_df.merge(
    repairs_df,
    on="repair_id",
    how="left",
    suffixes=(
        "_followup",
        "_repair"
    )
)


total_calls = len(
    merged_df
)


scheduled_calls = (
    merged_df["call_status"]
    .astype(str)
    .eq("Scheduled")
    .sum()
    if "call_status" in merged_df.columns
    else 0
)


completed_calls = (
    merged_df["call_status"]
    .astype(str)
    .eq("Completed")
    .sum()
    if "call_status" in merged_df.columns
    else 0
)


issue_calls = (
    merged_df["issue_detected"]
    .astype(str)
    .str.lower()
    .isin(
        [
            "true",
            "yes",
            "1"
        ]
    )
    .sum()
    if "issue_detected" in merged_df.columns
    else 0
)


m1, m2, m3, m4 = st.columns(
    4
)

m1.metric(
    "Total Follow-ups",
    total_calls
)

m2.metric(
    "Scheduled",
    scheduled_calls
)

m3.metric(
    "Completed",
    completed_calls
)

m4.metric(
    "Issues Detected",
    issue_calls
)


st.divider()


tab1, tab2, tab3 = st.tabs(
    [
        "Scheduled",
        "Completed",
        "All Calls"
    ]
)


with tab1:

    scheduled_df = merged_df[
        merged_df[
            "call_status"
        ].astype(str)
        == "Scheduled"
    ]


    if scheduled_df.empty:

        st.info(
            "No scheduled follow-up calls."
        )

    else:

        scheduled_ids = (
            scheduled_df[
                "followup_id"
            ]
            .dropna()
            .astype(str)
            .tolist()
        )


        selected_followup = st.selectbox(
            "Select Follow-up",
            scheduled_ids,
            key="scheduled_followup_select"
        )


        selected_rows = scheduled_df[
            scheduled_df[
                "followup_id"
            ].astype(str)
            == str(
                selected_followup
            )
        ]


        if not selected_rows.empty:

            row = selected_rows.iloc[0]


            st.write("")


            left, right = st.columns(
                2
            )


            with left:

                st.write(
                    f"**Customer:** "
                    f"{row.get('customer_name_followup', row.get('customer_name', 'Customer'))}"
                )

                st.write(
                    f"**Device:** "
                    f"{row.get('device', 'Device')}"
                )

                st.write(
                    f"**Repair:** "
                    f"{row.get('repair_type', 'Repair')}"
                )


            with right:

                st.write(
                    f"**Repair ID:** "
                    f"{row.get('repair_id', '')}"
                )

                st.write(
                    f"**Phone:** "
                    f"{row.get('phone', '')}"
                )

                st.write(
                    f"**Follow-up ID:** "
                    f"{row.get('followup_id', '')}"
                )


            st.write("")


            call_mode = st.radio(
                "Call Mode",
                [
                    "Demo Simulation",
                    "Live CALL-E"
                ],
                horizontal=True,
                key=f"mode_{selected_followup}"
            )


            scenario = "issue"


            if call_mode == "Demo Simulation":

                scenario = st.selectbox(
                    "Demo Scenario",
                    [
                        "healthy",
                        "issue",
                        "critical"
                    ],
                    key=f"scenario_{selected_followup}"
                )


            if call_mode == "Live CALL-E":

                st.warning(
                    "This will place a real CALL-E call "
                    "to the customer phone number."
                )


            button_text = (
                "📞 Place Live CALL-E Call"
                if call_mode == "Live CALL-E"
                else "▶ Run Demo Follow-up"
            )


            if st.button(
                button_text,
                type="primary",
                use_container_width=True,
                key=f"call_{selected_followup}"
            ):

                try:

                    with st.spinner(
                        "Running follow-up call..."
                    ):

                        customer_name = (
                            row.get(
                                "customer_name_repair"
                            )
                            or row.get(
                                "customer_name_followup"
                            )
                            or row.get(
                                "customer_name"
                            )
                            or "Customer"
                        )


                        repair_data = {
                            "repair_id":
                                row.get(
                                    "repair_id",
                                    ""
                                ),

                            "customer_name":
                                customer_name,

                            "phone":
                                row.get(
                                    "phone",
                                    ""
                                ),

                            "device":
                                row.get(
                                    "device",
                                    "Device"
                                ),

                            "repair_type":
                                row.get(
                                    "repair_type",
                                    "Repair"
                                )
                        }


                        call_result = (
                            make_followup_call(
                                repair=repair_data,
                                test_mode=(
                                    call_mode
                                    == "Demo Simulation"
                                ),
                                scenario=scenario
                            )
                        )


                        analysis = (
                            analyze_call_result(
                                call_result,
                                repair=repair_data
                            )
                        )


                        risk_result = (
                            calculate_risk_score(
                                analysis.get(
                                    "issue_detected",
                                    False
                                ),
                                analysis.get(
                                    "severity",
                                    "Low"
                                ),
                                analysis.get(
                                    "sentiment",
                                    "Neutral"
                                ),
                                analysis.get(
                                    "warranty_related",
                                    False
                                ),
                                analysis.get(
                                    "safety_issue",
                                    False
                                ),
                                analysis.get(
                                    "repeat_issue",
                                    False
                                )
                            )
                        )


                        if isinstance(
                            risk_result,
                            tuple
                        ):

                            risk_score = (
                                risk_result[0]
                            )

                            risk_action = (
                                risk_result[1]
                                if len(
                                    risk_result
                                ) > 1
                                else ""
                            )

                        elif isinstance(
                            risk_result,
                            dict
                        ):

                            risk_score = (
                                risk_result.get(
                                    "risk_score",
                                    risk_result.get(
                                        "score",
                                        0
                                    )
                                )
                            )

                            risk_action = (
                                risk_result.get(
                                    "recommendation",
                                    risk_result.get(
                                        "action",
                                        ""
                                    )
                                )
                            )

                        else:

                            risk_score = (
                                risk_result
                            )

                            risk_action = ""


                        updated_df = safe_read_csv(
                            FOLLOWUPS_FILE
                        )


                        mask = (
                            updated_df[
                                "followup_id"
                            ].astype(str)
                            == str(
                                selected_followup
                            )
                        )


                        text_columns = [
                            "call_status",
                            "health_status",
                            "issue_category",
                            "issue_summary",
                            "severity",
                            "sentiment",
                            "recommended_action"
                        ]


                        for column in text_columns:

                            updated_df = (
                                prepare_text_column(
                                    updated_df,
                                    column
                                )
                            )


                        other_columns = [
                            "issue_detected",
                            "risk_score",
                            "ticket_required"
                        ]


                        for column in other_columns:

                            if column not in updated_df.columns:
                                updated_df[column] = ""

                            updated_df[column] = (
                                updated_df[column]
                                .astype("object")
                            )


                        updated_df.loc[
                            mask,
                            "call_status"
                        ] = "Completed"


                        updated_df.loc[
                            mask,
                            "issue_detected"
                        ] = (
                            "Yes"
                            if analysis.get(
                                "issue_detected",
                                False
                            )
                            else "No"
                        )


                        updated_df.loc[
                            mask,
                            "severity"
                        ] = analysis.get(
                            "severity",
                            "Low"
                        )


                        updated_df.loc[
                            mask,
                            "sentiment"
                        ] = analysis.get(
                            "sentiment",
                            "Neutral"
                        )


                        updated_df.loc[
                            mask,
                            "risk_score"
                        ] = risk_score


                        updated_df.loc[
                            mask,
                            "recommended_action"
                        ] = str(
                            risk_action
                        )


                        updated_df.loc[
                            mask,
                            "ticket_required"
                        ] = (
                            "Yes"
                            if analysis.get(
                                "ticket_required",
                                False
                            )
                            else "No"
                        )


                        if analysis.get(
                            "issue_detected",
                            False
                        ):

                            updated_df.loc[
                                mask,
                                "health_status"
                            ] = "Issue Detected"

                        else:

                            updated_df.loc[
                                mask,
                                "health_status"
                            ] = "Healthy"


                        if "issue_category" in updated_df.columns:

                            updated_df.loc[
                                mask,
                                "issue_category"
                            ] = analysis.get(
                                "issue_category",
                                "None"
                            )


                        if "issue_summary" in updated_df.columns:

                            updated_df.loc[
                                mask,
                                "issue_summary"
                            ] = analysis.get(
                                "issue_summary",
                                ""
                            )


                        save_followups(
                            updated_df
                        )


                        update_customer_health(
                            repair_id=
                                repair_data[
                                    "repair_id"
                                ],

                            customer_name=
                                repair_data[
                                    "customer_name"
                                ],

                            risk_score=
                                risk_score,

                            severity=
                                analysis.get(
                                    "severity",
                                    "Low"
                                )
                        )


                        ticket = None
                        recovery = None


                        if analysis.get(
                            "ticket_required",
                            False
                        ):

                            ticket = create_ticket(
                                repair_id=
                                    repair_data[
                                        "repair_id"
                                    ],

                                customer_name=
                                    repair_data[
                                        "customer_name"
                                    ],

                                issue=
                                    analysis.get(
                                        "issue_summary",
                                        ""
                                    ),

                                severity=
                                    analysis.get(
                                        "severity",
                                        "Medium"
                                    ),

                                risk_score=
                                    risk_score,

                                warranty_related=
                                    analysis.get(
                                        "warranty_related",
                                        False
                                    ),

                                safety_issue=
                                    analysis.get(
                                        "safety_issue",
                                        False
                                    )
                            )


                            if ticket:

                                ticket_id = (
                                    ticket.get(
                                        "ticket_id"
                                    )
                                    if isinstance(
                                        ticket,
                                        dict
                                    )
                                    else None
                                )


                                priority = (
                                    ticket.get(
                                        "priority",
                                        "P1"
                                    )
                                    if isinstance(
                                        ticket,
                                        dict
                                    )
                                    else "P1"
                                )


                                assigned_team = (
                                    ticket.get(
                                        "assigned_team",
                                        "Technician Team"
                                    )
                                    if isinstance(
                                        ticket,
                                        dict
                                    )
                                    else "Technician Team"
                                )


                                if ticket_id:

                                    recovery = (
                                        create_recovery_case(
                                            ticket_id=
                                                ticket_id,

                                            repair_id=
                                                repair_data[
                                                    "repair_id"
                                                ],

                                            customer_name=
                                                repair_data[
                                                    "customer_name"
                                                ],

                                            assigned_to=
                                                assigned_team,

                                            resolution_type=
                                                "Technician Revisit",

                                            priority=
                                                priority
                                        )
                                    )


                    if analysis.get(
                        "issue_detected",
                        False
                    ):

                        st.error(
                            "⚠️ Post-service issue detected."
                        )

                    else:

                        st.success(
                            "✅ Service verified. "
                            "Customer reported no issue."
                        )


                    st.subheader(
                        "AI Decision"
                    )


                    st.json(
                        {
                            "Issue Detected":
                                analysis.get(
                                    "issue_detected"
                                ),

                            "Issue Category":
                                analysis.get(
                                    "issue_category"
                                ),

                            "Issue Summary":
                                analysis.get(
                                    "issue_summary"
                                ),

                            "Severity":
                                analysis.get(
                                    "severity"
                                ),

                            "Sentiment":
                                analysis.get(
                                    "sentiment"
                                ),

                            "Warranty Related":
                                analysis.get(
                                    "warranty_related"
                                ),

                            "Safety Issue":
                                analysis.get(
                                    "safety_issue"
                                ),

                            "Repeat Issue":
                                analysis.get(
                                    "repeat_issue"
                                ),

                            "Risk Score":
                                risk_score,

                            "Recommended Action":
                                risk_action,

                            "Ticket Required":
                                analysis.get(
                                    "ticket_required"
                                )
                        }
                    )


                    if ticket:

                        st.success(
                            "🎫 Ticket created automatically."
                        )

                        if isinstance(
                            ticket,
                            dict
                        ):

                            st.write(
                                f"**Ticket ID:** "
                                f"{ticket.get('ticket_id', '')}"
                            )


                    if recovery:

                        st.success(
                            "🛠️ Recovery case created automatically."
                        )

                        if isinstance(
                            recovery,
                            dict
                        ):

                            st.write(
                                f"**Recovery ID:** "
                                f"{recovery.get('resolution_id', '')}"
                            )


                    with st.expander(
                        "📄 CALL-E Transcript"
                    ):

                        transcript = (
                            call_result.get(
                                "transcript",
                                []
                            )
                        )

                        if transcript:

                            for turn in transcript:

                                speaker = str(
                                    turn.get(
                                        "speaker",
                                        ""
                                    )
                                ).upper()

                                text = str(
                                    turn.get(
                                        "text",
                                        ""
                                    )
                                )

                                st.write(
                                    f"**{speaker}:** {text}"
                                )

                        else:

                            st.write(
                                "No transcript available."
                            )


                    with st.expander(
                        "Raw CALL-E Result"
                    ):

                        st.json(
                            call_result
                        )


                    st.success(
                        "Follow-up processing completed."
                    )


                    if st.button(
                        "Refresh Follow-up Calls",
                        key=f"refresh_{selected_followup}"
                    ):

                        st.rerun()


                except Exception as e:

                    st.error(
                        f"Call failed: {e}"
                    )


with tab2:

    completed_df = merged_df[
        merged_df[
            "call_status"
        ].astype(str)
        == "Completed"
    ]


    if completed_df.empty:

        st.info(
            "No completed follow-up calls."
        )

    else:

        display_columns = [
            column
            for column in [
                "followup_id",
                "repair_id",
                "customer_name_followup",
                "device",
                "repair_type",
                "issue_detected",
                "severity",
                "sentiment",
                "risk_score"
            ]
            if column in completed_df.columns
        ]


        st.dataframe(
            completed_df[
                display_columns
            ],
            use_container_width=True,
            hide_index=True
        )


with tab3:

    display_columns = [
        column
        for column in [
            "followup_id",
            "repair_id",
            "customer_name_followup",
            "device",
            "repair_type",
            "call_status",
            "health_status",
            "issue_detected",
            "severity",
            "risk_score",
            "recommended_action",
            "ticket_required"
        ]
        if column in merged_df.columns
    ]


    st.dataframe(
        merged_df[
            display_columns
        ],
        use_container_width=True,
        hide_index=True
    )