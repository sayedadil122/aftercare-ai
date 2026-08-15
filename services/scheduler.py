import pandas as pd
from datetime import datetime, timedelta


REPAIRS_FILE = "data/repairs.csv"


FOLLOWUP_DELAY_HOURS = {
    "Screen Replacement": 4,
    "Display Repair": 4,
    "Battery Replacement": 8,
    "Charging Port Repair": 6,
    "Camera Repair": 6,
    "Water Damage Repair": 24
}


def calculate_followup_time(
    completed_at,
    repair_type
):
    completed_time = pd.to_datetime(
        completed_at
    )

    delay_hours = FOLLOWUP_DELAY_HOURS.get(
        repair_type,
        6
    )

    return completed_time + timedelta(
        hours=delay_hours
    )


def schedule_missing_followups():
    repairs_df = pd.read_csv(REPAIRS_FILE)

    if "followup_time" not in repairs_df.columns:
        repairs_df["followup_time"] = ""

    for index, row in repairs_df.iterrows():

        followup_value = row.get(
            "followup_time",
            ""
        )

        if (
            pd.isna(followup_value)
            or str(followup_value).strip() == ""
        ):

            scheduled_time = calculate_followup_time(
                row["completed_at"],
                row["repair_type"]
            )

            repairs_df.at[
                index,
                "followup_time"
            ] = scheduled_time.strftime(
                "%Y-%m-%d %H:%M"
            )

    repairs_df.to_csv(
        REPAIRS_FILE,
        index=False
    )

    return repairs_df


def get_due_followups():

    schedule_missing_followups()

    repairs_df = pd.read_csv(
        REPAIRS_FILE
    )

    repairs_df["followup_time"] = pd.to_datetime(
        repairs_df["followup_time"]
    )

    now = pd.Timestamp(
        datetime.now()
    )

    due_df = repairs_df[
        (
            repairs_df["status"]
            == "Completed"
        )
        &
        (
            repairs_df["followup_time"]
            <= now
        )
    ].copy()

    return due_df


def get_next_followups():

    schedule_missing_followups()

    repairs_df = pd.read_csv(
        REPAIRS_FILE
    )

    repairs_df["followup_time"] = pd.to_datetime(
        repairs_df["followup_time"]
    )

    now = pd.Timestamp(
        datetime.now()
    )

    upcoming_df = repairs_df[
        (
            repairs_df["status"]
            == "Completed"
        )
        &
        (
            repairs_df["followup_time"]
            > now
        )
    ].copy()

    upcoming_df = upcoming_df.sort_values(
        by="followup_time"
    )

    return upcoming_df