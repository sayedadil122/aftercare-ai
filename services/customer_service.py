import os
import pandas as pd


CUSTOMERS_FILE = "data/customers.csv"


def load_customers():
    if not os.path.exists(CUSTOMERS_FILE):
        return pd.DataFrame()

    try:
        return pd.read_csv(CUSTOMERS_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def save_customers(df):
    df.to_csv(
        CUSTOMERS_FILE,
        index=False
    )


def update_customer_health(
    customer_name=None,
    health_status=None,
    risk_score=0,
    severity="Low",
    repair_id=None,
    **kwargs
):
    df = load_customers()

    if df.empty:
        return False

    if "health_status" not in df.columns:
        df["health_status"] = ""

    if "risk_score" not in df.columns:
        df["risk_score"] = 0

    if "severity" not in df.columns:
        df["severity"] = ""

    df["health_status"] = df[
        "health_status"
    ].astype("object")

    df["severity"] = df[
        "severity"
    ].astype("object")

    mask = pd.Series(
        False,
        index=df.index
    )

    if (
        repair_id
        and "repair_id" in df.columns
    ):
        mask = (
            df["repair_id"]
            .astype(str)
            == str(repair_id)
        )

    if (
        not mask.any()
        and customer_name
        and "customer_name" in df.columns
    ):
        mask = (
            df["customer_name"]
            .astype(str)
            == str(customer_name)
        )

    if not mask.any():
        return False

    if health_status is None:
        severity_text = str(
            severity
        ).lower()

        try:
            score = float(
                risk_score
            )
        except Exception:
            score = 0

        if (
            severity_text == "critical"
            or score >= 80
        ):
            health_status = "Critical"

        elif (
            severity_text == "high"
            or score >= 60
        ):
            health_status = "At Risk"

        elif score >= 30:
            health_status = "Monitor"

        else:
            health_status = "Healthy"

    df.loc[
        mask,
        "health_status"
    ] = health_status

    df.loc[
        mask,
        "risk_score"
    ] = risk_score

    df.loc[
        mask,
        "severity"
    ] = severity

    save_customers(df)

    return True