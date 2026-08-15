import os
from datetime import datetime

import pandas as pd


TICKETS_FILE = "data/tickets.csv"


def load_tickets():
    if not os.path.exists(TICKETS_FILE):
        return pd.DataFrame()
    try:
        return pd.read_csv(TICKETS_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def save_tickets(df):
    df.to_csv(TICKETS_FILE, index=False)


def get_priority(severity="Medium", risk_score=0, safety_issue=False, **kwargs):
    try:
        score = int(float(risk_score))
    except Exception:
        score = 0
    severity = str(severity).strip().lower()
    if safety_issue or severity == "critical" or score >= 80:
        return "P0"
    if severity == "high" or score >= 60:
        return "P1"
    if severity == "medium" or score >= 30:
        return "P2"
    return "P3"


def get_assigned_team(priority="P2", *args, **kwargs):
    priority = str(priority).strip().upper()
    if priority == "P0":
        return "Senior Technician"
    if priority in ["P1", "P2"]:
        return "Technician Team"
    return "Support Team"


def generate_ticket_id(df):
    if df.empty or "ticket_id" not in df.columns:
        return "T001"
    numbers = []
    for value in df["ticket_id"].dropna().astype(str):
        digits = "".join(c for c in value if c.isdigit())
        if digits:
            numbers.append(int(digits))
    return f"T{max(numbers) + 1 if numbers else 1:03d}"


def create_ticket(repair_id, customer_name, issue, severity="Medium", risk_score=0,
                  warranty_related=False, safety_issue=False, priority=None,
                  assigned_team=None, status=None, **kwargs):
    df = load_tickets()
    if not df.empty and "repair_id" in df.columns:
        existing = df[df["repair_id"].astype(str) == str(repair_id)]
        if not existing.empty:
            return existing.iloc[0].to_dict()

    if priority is None:
        priority = get_priority(severity, risk_score, safety_issue)
    if assigned_team is None:
        assigned_team = get_assigned_team(priority)
    if status is None:
        status = "Escalated" if priority == "P0" else "Open"

    warranty_review = "Required" if warranty_related else "Not Required"
    if priority == "P0":
        next_action = "Immediate escalation"
    elif warranty_related:
        next_action = "Warranty review + Technician follow-up"
    else:
        next_action = "Technician follow-up"

    try:
        risk_score = int(float(risk_score))
    except Exception:
        risk_score = 0

    columns = [
        "ticket_id", "repair_id", "customer_name", "issue", "severity",
        "risk_score", "priority", "status", "assigned_team",
        "warranty_review", "safety_issue", "next_action", "created_at"
    ]
    for column in columns:
        if column not in df.columns:
            df[column] = ""

    ticket = {
        "ticket_id": generate_ticket_id(df),
        "repair_id": repair_id,
        "customer_name": customer_name,
        "issue": issue,
        "severity": severity,
        "risk_score": risk_score,
        "priority": priority,
        "status": status,
        "assigned_team": assigned_team,
        "warranty_review": warranty_review,
        "safety_issue": bool(safety_issue),
        "next_action": next_action,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    new_df = pd.DataFrame([ticket])
    df = new_df if df.empty else pd.concat([df, new_df], ignore_index=True)
    save_tickets(df)
    return ticket


def get_ticket_by_repair(repair_id):
    df = load_tickets()
    if df.empty or "repair_id" not in df.columns:
        return None
    result = df[df["repair_id"].astype(str) == str(repair_id)]
    return None if result.empty else result.iloc[0].to_dict()


def update_ticket_status(ticket_id, status, next_action=None, **kwargs):
    df = load_tickets()
    if df.empty or "ticket_id" not in df.columns:
        return False
    mask = df["ticket_id"].astype(str) == str(ticket_id)
    if not mask.any():
        return False
    df["status"] = df.get("status", "").astype("object") if "status" in df else ""
    df.loc[mask, "status"] = status
    if next_action is not None:
        if "next_action" not in df.columns:
            df["next_action"] = ""
        df["next_action"] = df["next_action"].astype("object")
        df.loc[mask, "next_action"] = next_action
    save_tickets(df)
    return True


def resolve_ticket(ticket_id, **kwargs):
    return update_ticket_status(ticket_id, "Resolved", "Case closed after customer verification")


def escalate_ticket(ticket_id, **kwargs):
    return update_ticket_status(ticket_id, "Escalated", "Senior technician escalation required")
