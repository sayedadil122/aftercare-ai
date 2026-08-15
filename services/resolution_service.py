import os
from datetime import datetime

import pandas as pd


# =========================================================
# FILE PATHS
# =========================================================

RESOLUTIONS_FILE = "data/resolutions.csv"
TICKETS_FILE = "data/tickets.csv"
CUSTOMERS_FILE = "data/customers.csv"


# =========================================================
# HELPERS
# =========================================================

def current_time():
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )


def safe_read_csv(file_path):

    if not os.path.exists(file_path):
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path)

    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def ensure_column(
    df,
    column_name,
    default_value=""
):

    if column_name not in df.columns:
        df[column_name] = default_value

    return df


def prepare_text_column(
    df,
    column_name
):

    df = ensure_column(
        df,
        column_name,
        ""
    )

    df[column_name] = (
        df[column_name]
        .astype("object")
    )

    return df


def save_csv(
    df,
    file_path
):

    df.to_csv(
        file_path,
        index=False
    )


def generate_resolution_id(df):

    if df.empty:
        return "RS001"

    if "resolution_id" not in df.columns:
        return "RS001"

    numbers = []

    for value in (
        df["resolution_id"]
        .dropna()
        .astype(str)
    ):

        digits = "".join(
            char
            for char in value
            if char.isdigit()
        )

        if digits:
            numbers.append(
                int(digits)
            )

    next_number = (
        max(numbers) + 1
        if numbers
        else 1
    )

    return f"RS{next_number:03d}"


# =========================================================
# CREATE RECOVERY CASE
# =========================================================

def create_recovery_case(
    ticket_id,
    repair_id,
    customer_name,
    assigned_to="Technician Team",
    resolution_type="Technician Revisit",
    priority="P1",
    **kwargs
):

    df = safe_read_csv(
        RESOLUTIONS_FILE
    )

    # Duplicate protection
    if (
        not df.empty
        and "ticket_id" in df.columns
    ):

        existing = df[
            df["ticket_id"].astype(str)
            == str(ticket_id)
        ]

        if not existing.empty:
            return (
                existing
                .iloc[0]
                .to_dict()
            )


    columns = [
        "resolution_id",
        "ticket_id",
        "repair_id",
        "customer_name",
        "resolution_type",
        "assigned_to",
        "priority",
        "status",
        "created_at",
        "started_at",
        "resolved_at",
        "verification_call_id",
        "customer_confirmed",
        "final_csat",
        "verification_feedback",
        "verified_at"
    ]


    for column in columns:

        df = ensure_column(
            df,
            column,
            ""
        )


    resolution_id = (
        generate_resolution_id(
            df
        )
    )


    new_row = {

        "resolution_id":
            resolution_id,

        "ticket_id":
            ticket_id,

        "repair_id":
            repair_id,

        "customer_name":
            customer_name,

        "resolution_type":
            resolution_type,

        "assigned_to":
            assigned_to,

        "priority":
            priority,

        "status":
            "Scheduled",

        "created_at":
            current_time(),

        "started_at":
            "",

        "resolved_at":
            "",

        "verification_call_id":
            "",

        "customer_confirmed":
            "",

        "final_csat":
            "",

        "verification_feedback":
            "",

        "verified_at":
            ""
    }


    df = pd.concat(
        [
            df,
            pd.DataFrame(
                [new_row]
            )
        ],
        ignore_index=True
    )


    save_csv(
        df,
        RESOLUTIONS_FILE
    )


    return new_row


# =========================================================
# OLD NAME COMPATIBILITY
# =========================================================

def create_resolution_case(
    ticket_id,
    repair_id,
    customer_name,
    assigned_to="Technician Team",
    resolution_type="Technician Revisit",
    priority="P1",
    **kwargs
):

    return create_recovery_case(
        ticket_id=ticket_id,
        repair_id=repair_id,
        customer_name=customer_name,
        assigned_to=assigned_to,
        resolution_type=resolution_type,
        priority=priority
    )


# =========================================================
# START TECHNICIAN RECOVERY
# =========================================================

def mark_resolution_in_progress(
    resolution_id
):

    df = safe_read_csv(
        RESOLUTIONS_FILE
    )

    if df.empty:

        raise ValueError(
            "No recovery cases found."
        )


    if "resolution_id" not in df.columns:

        raise ValueError(
            "resolution_id column missing."
        )


    mask = (
        df["resolution_id"]
        .astype(str)
        == str(resolution_id)
    )


    if not mask.any():

        raise ValueError(
            f"Recovery case {resolution_id} not found."
        )


    df = prepare_text_column(
        df,
        "status"
    )

    df = prepare_text_column(
        df,
        "started_at"
    )


    df.loc[
        mask,
        "status"
    ] = "In Progress"


    df.loc[
        mask,
        "started_at"
    ] = current_time()


    save_csv(
        df,
        RESOLUTIONS_FILE
    )


    return {

        "resolution_id":
            resolution_id,

        "status":
            "In Progress"
    }


# =========================================================
# TECHNICIAN WORK COMPLETE
# =========================================================

def mark_resolution_completed(
    resolution_id
):

    df = safe_read_csv(
        RESOLUTIONS_FILE
    )


    if df.empty:

        raise ValueError(
            "No recovery cases found."
        )


    if "resolution_id" not in df.columns:

        raise ValueError(
            "resolution_id column missing."
        )


    mask = (
        df["resolution_id"]
        .astype(str)
        == str(resolution_id)
    )


    if not mask.any():

        raise ValueError(
            f"Recovery case {resolution_id} not found."
        )


    # Important pandas datatype fix
    df = prepare_text_column(
        df,
        "status"
    )

    df = prepare_text_column(
        df,
        "resolved_at"
    )


    df.loc[
        mask,
        "status"
    ] = "Resolved"


    completed_time = (
        current_time()
    )


    df.loc[
        mask,
        "resolved_at"
    ] = completed_time


    save_csv(
        df,
        RESOLUTIONS_FILE
    )


    return {

        "resolution_id":
            resolution_id,

        "status":
            "Resolved",

        "resolved_at":
            completed_time
    }


# =========================================================
# UPDATE TICKET AFTER VERIFICATION
# =========================================================

def update_ticket_after_verification(
    ticket_id,
    customer_confirmed
):

    df = safe_read_csv(
        TICKETS_FILE
    )


    if df.empty:
        return


    if "ticket_id" not in df.columns:
        return


    mask = (
        df["ticket_id"]
        .astype(str)
        == str(ticket_id)
    )


    if not mask.any():
        return


    df = prepare_text_column(
        df,
        "status"
    )

    df = prepare_text_column(
        df,
        "next_action"
    )


    if customer_confirmed:

        df.loc[
            mask,
            "status"
        ] = "Resolved"

        df.loc[
            mask,
            "next_action"
        ] = (
            "Case closed after "
            "customer verification"
        )

    else:

        df.loc[
            mask,
            "status"
        ] = "Escalated"

        df.loc[
            mask,
            "next_action"
        ] = (
            "Senior technician escalation required"
        )


    save_csv(
        df,
        TICKETS_FILE
    )


# =========================================================
# UPDATE CUSTOMER HEALTH
# =========================================================

def update_customer_after_verification(
    repair_id,
    customer_name,
    customer_confirmed
):

    df = safe_read_csv(
        CUSTOMERS_FILE
    )


    if df.empty:
        return


    df = prepare_text_column(
        df,
        "health_status"
    )


    mask = pd.Series(
        False,
        index=df.index
    )


    if (
        "repair_id" in df.columns
        and repair_id
    ):

        mask = (
            df["repair_id"]
            .astype(str)
            == str(repair_id)
        )


    if (
        not mask.any()
        and "customer_name"
        in df.columns
    ):

        mask = (
            df["customer_name"]
            .astype(str)
            == str(customer_name)
        )


    if not mask.any():
        return


    if customer_confirmed:

        df.loc[
            mask,
            "health_status"
        ] = "Healthy"

    else:

        df.loc[
            mask,
            "health_status"
        ] = "Critical"


    save_csv(
        df,
        CUSTOMERS_FILE
    )


# =========================================================
# SAVE SECOND CALL-E VERIFICATION
# =========================================================

def save_verification_result(
    resolution_id,
    customer_confirmed,
    final_csat=3,
    call_id="",
    feedback="",
    **kwargs
):

    df = safe_read_csv(
        RESOLUTIONS_FILE
    )


    if df.empty:

        raise ValueError(
            "No recovery cases found."
        )


    if "resolution_id" not in df.columns:

        raise ValueError(
            "resolution_id column missing."
        )


    mask = (
        df["resolution_id"]
        .astype(str)
        == str(resolution_id)
    )


    if not mask.any():

        raise ValueError(
            f"Recovery case {resolution_id} not found."
        )


    case = (
        df[
            mask
        ]
        .iloc[0]
    )


    ticket_id = case.get(
        "ticket_id",
        ""
    )

    repair_id = case.get(
        "repair_id",
        ""
    )

    customer_name = case.get(
        "customer_name",
        ""
    )


    text_columns = [
        "status",
        "verification_call_id",
        "customer_confirmed",
        "verification_feedback",
        "verified_at"
    ]


    for column in text_columns:

        df = prepare_text_column(
            df,
            column
        )


    df = ensure_column(
        df,
        "final_csat",
        ""
    )

    df["final_csat"] = (
        df["final_csat"]
        .astype("object")
    )


    confirmed = bool(
        customer_confirmed
    )


    if confirmed:

        new_status = "Resolved"

    else:

        new_status = "Reopened"


    df.loc[
        mask,
        "status"
    ] = new_status


    df.loc[
        mask,
        "customer_confirmed"
    ] = (
        "Yes"
        if confirmed
        else "No"
    )


    df.loc[
        mask,
        "final_csat"
    ] = final_csat


    df.loc[
        mask,
        "verification_call_id"
    ] = str(
        call_id or ""
    )


    df.loc[
        mask,
        "verification_feedback"
    ] = str(
        feedback or ""
    )


    df.loc[
        mask,
        "verified_at"
    ] = current_time()


    save_csv(
        df,
        RESOLUTIONS_FILE
    )


    # Ticket sync
    update_ticket_after_verification(
        ticket_id=
            ticket_id,

        customer_confirmed=
            confirmed
    )


    # Customer health sync
    update_customer_after_verification(
        repair_id=
            repair_id,

        customer_name=
            customer_name,

        customer_confirmed=
            confirmed
    )


    return {

        "resolution_id":
            resolution_id,

        "status":
            new_status,

        "customer_confirmed":
            confirmed,

        "final_csat":
            final_csat,

        "ticket_id":
            ticket_id,

        "repair_id":
            repair_id
    }


# =========================================================
# REOPEN RECOVERY
# =========================================================

def reopen_resolution(
    resolution_id
):

    df = safe_read_csv(
        RESOLUTIONS_FILE
    )


    if df.empty:

        raise ValueError(
            "No recovery cases found."
        )


    mask = (
        df["resolution_id"]
        .astype(str)
        == str(resolution_id)
    )


    if not mask.any():

        raise ValueError(
            f"Recovery case {resolution_id} not found."
        )


    df = prepare_text_column(
        df,
        "status"
    )


    df.loc[
        mask,
        "status"
    ] = "Reopened"


    save_csv(
        df,
        RESOLUTIONS_FILE
    )


    return {

        "resolution_id":
            resolution_id,

        "status":
            "Reopened"
    }


# =========================================================
# GET ONE RECOVERY CASE
# =========================================================

def get_resolution(
    resolution_id
):

    df = safe_read_csv(
        RESOLUTIONS_FILE
    )


    if df.empty:
        return None


    if "resolution_id" not in df.columns:
        return None


    rows = df[
        df["resolution_id"]
        .astype(str)
        == str(resolution_id)
    ]


    if rows.empty:
        return None


    return (
        rows.iloc[0]
        .to_dict()
    )


# =========================================================
# OLD DEMO FUNCTION COMPATIBILITY
# =========================================================

def simulate_verification_call(
    resolution_id=None,
    scenario="resolved",
    **kwargs
):

    if scenario in [
        "resolved",
        "healthy",
        "success"
    ]:

        return {

            "call_id":
                f"VERIFY-DEMO-{resolution_id}",

            "status":
                "completed",

            "issue_resolved":
                True,

            "customer_confirmed":
                True,

            "final_csat":
                5,

            "feedback":
                "Customer confirmed the issue is resolved.",

            "transcript": []
        }


    return {

        "call_id":
            f"VERIFY-DEMO-{resolution_id}",

        "status":
            "completed",

        "issue_resolved":
            False,

        "customer_confirmed":
            False,

        "final_csat":
            2,

        "feedback":
            "Customer confirmed the issue is unresolved.",

        "transcript": []
    }