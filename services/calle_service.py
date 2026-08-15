import os
import time
from datetime import datetime

from dotenv import load_dotenv
from calle import CalleClient


load_dotenv()


CALLE_API_KEY = os.getenv("CALLE_API_KEY")


RESULT_SCHEMA = {
    "type": "object",
    "required": [
        "issue_detected",
        "issue_summary",
        "severity",
        "sentiment"
    ],
    "properties": {
        "issue_detected": {
            "type": "boolean"
        },
        "issue_summary": {
            "type": "string"
        },
        "severity": {
            "type": "string",
            "enum": [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        },
        "sentiment": {
            "type": "string",
            "enum": [
                "Positive",
                "Neutral",
                "Negative"
            ]
        }
    }
}


def normalize_phone(phone):

    phone = str(phone or "").strip()

    phone = (
        phone
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )

    if phone.startswith("91") and not phone.startswith("+"):
        phone = "+" + phone

    if not phone.startswith("+"):
        raise ValueError(
            "Phone must be E.164 format. "
            "Example: +916386351022"
        )

    return phone


def build_followup_task(repair):

    phone = normalize_phone(
        repair.get("phone")
    )

    customer_name = repair.get(
        "customer_name",
        "Customer"
    )

    device = repair.get(
        "device",
        "device"
    )

    repair_type = repair.get(
        "repair_type",
        "repair"
    )

    return f"""
Call {phone}.

You are AfterCare AI.

Speak with {customer_name} regarding their recent repair.

Device: {device}
Repair: {repair_type}

Start by saying:

"Hello {customer_name}, this is AfterCare AI.
I am calling regarding your recent {repair_type}
for your {device}. I wanted to quickly check
how the device is working after the repair."

Then ask:

"Is the repaired device working properly now?"

Wait for the customer's response.

If the customer says the device is working fine:

Ask:

"Have you noticed any unusual problem since the repair?"

If they say no:

Thank them and end the call politely.

If the customer reports a problem:

Ask only relevant follow-up questions:

- What exactly is happening?
- When did it start?
- Is it affecting the repaired part?
- Was there any new physical damage?
- Was there any water exposure?
- Is the phone overheating?
- Is there smoke?
- Is there battery swelling?
- Is there an electrical or burning smell?

Do not promise:
- refunds
- warranty approval
- free repairs
- free replacement

If there is an issue, tell the customer:

"Thank you for explaining the issue.
I will share this with our service team for review."

Then end politely.

For the final result:

issue_detected:
false if customer confirms everything is working normally.
true if customer reports any post-service problem.

severity:
Low = minor inconvenience
Medium = noticeable issue
High = major functional issue
Critical = safety issue such as severe overheating,
smoke, swelling or electrical smell.

sentiment:
Positive, Neutral or Negative.

Use only what the customer actually says.
""".strip()


def extract_transcript(call):

    transcript = []

    for recipient in call.get("recipients", []):

        for attempt in recipient.get(
            "attempts",
            []
        ):

            turns = attempt.get(
                "transcript_turns",
                []
            )

            transcript.extend(turns)

    return transcript


def extract_structured_result(call):

    # First check recipient result
    for recipient in call.get(
        "recipients",
        []
    ):

        result = recipient.get(
            "structured_result"
        )

        if isinstance(result, dict) and result:
            return result

    # Then top-level result
    result = call.get(
        "structured_result"
    )

    if isinstance(result, dict) and result:
        return result

    return {}


def customer_text_from_transcript(
    transcript
):

    customer_lines = []

    for turn in transcript:

        speaker = str(
            turn.get("speaker", "")
        ).lower()

        text = str(
            turn.get("text", "")
        ).strip()

        if (
            speaker in [
                "user",
                "customer",
                "recipient"
            ]
            and text
        ):
            customer_lines.append(text)

    return " ".join(customer_lines).lower()


def transcript_fallback(
    transcript
):

    text = customer_text_from_transcript(
        transcript
    )

    if not text:
        raise RuntimeError(
            "No customer speech was captured."
        )

    safety_words = [
        "overheat",
        "overheating",
        "very hot",
        "smoke",
        "swelling",
        "swollen",
        "burning smell",
        "electrical smell",
        "fire"
    ]

    issue_words = [
        "not working",
        "problem",
        "issue",
        "freeze",
        "freezing",
        "broken",
        "not charging",
        "battery drain",
        "touch issue",
        "screen issue",
        "display issue",
        "heating",
        "restart"
    ]

    healthy_words = [
        "working fine",
        "working properly",
        "works fine",
        "all good",
        "no problem",
        "no issue",
        "everything is fine"
    ]

    safety_issue = any(
        word in text
        for word in safety_words
    )

    issue_detected = any(
        word in text
        for word in issue_words
    )

    healthy = any(
        word in text
        for word in healthy_words
    )

    if healthy and not issue_detected:
        issue_detected = False

    if safety_issue:
        severity = "Critical"

    elif issue_detected:
        severity = "High"

    else:
        severity = "Low"

    if any(
        x in text
        for x in [
            "angry",
            "bad",
            "problem",
            "not working",
            "worst",
            "frustrated"
        ]
    ):
        sentiment = "Negative"

    elif healthy:
        sentiment = "Positive"

    else:
        sentiment = "Neutral"

    if safety_issue:
        issue_category = "Heating"

    elif "battery" in text:
        issue_category = "Battery"

    elif "charging" in text:
        issue_category = "Charging"

    elif (
        "screen" in text
        or "touch" in text
        or "display" in text
    ):
        issue_category = "Screen"

    elif issue_detected:
        issue_category = "General"

    else:
        issue_category = "None"

    if issue_detected:
        issue_summary = (
            "Customer reported a post-service "
            f"{issue_category.lower()} issue."
        )

    else:
        issue_summary = (
            "Customer confirmed the repaired "
            "device is working properly."
        )

    return {
        "issue_detected":
            issue_detected,

        "issue_summary":
            issue_summary,

        "severity":
            severity,

        "sentiment":
            sentiment,

        "issue_category":
            issue_category,

        "safety_issue":
            safety_issue,

        "warranty_related":
            issue_detected,

        "repeat_issue":
            False
    }


def run_calle_call(repair):

    if not CALLE_API_KEY:
        raise ValueError(
            "CALLE_API_KEY missing in .env"
        )

    client = CalleClient(
        api_key=CALLE_API_KEY
    )

    return client.calls.create_and_wait(
        task=build_followup_task(
            repair
        ),
        result_schema=RESULT_SCHEMA
    )


def make_live_followup_call(
    repair
):

    last_error = None

    # One retry for transient CALL-E/provider failures
    for attempt_number in range(2):

        try:

            call = run_calle_call(
                repair
            )

            if not isinstance(
                call,
                dict
            ):

                try:
                    call = call.model_dump()

                except Exception:
                    call = dict(call)

            status = str(
                call.get(
                    "status",
                    ""
                )
            ).lower()

            if status != "completed":

                raise RuntimeError(
                    f"CALL-E returned status: {status}"
                )

            transcript = extract_transcript(
                call
            )

            if not transcript:

                raise RuntimeError(
                    "CALL-E completed but no transcript was captured."
                )

            result = extract_structured_result(
                call
            )

            fallback = transcript_fallback(
                transcript
            )

            # Structured result if available,
            # transcript analysis otherwise.
            issue_detected = result.get(
                "issue_detected",
                fallback["issue_detected"]
            )

            issue_summary = result.get(
                "issue_summary",
                fallback["issue_summary"]
            )

            severity = result.get(
                "severity",
                fallback["severity"]
            )

            sentiment = result.get(
                "sentiment",
                fallback["sentiment"]
            )

            return {
                "call_id":
                    call.get("id")
                    or call.get("call_id"),

                "status":
                    "completed",

                "task_completed":
                    call.get(
                        "task_completed",
                        True
                    ),

                "completion_confidence":
                    call.get(
                        "completion_confidence"
                    ),

                "completed_at":
                    datetime.now().isoformat(),

                "issue_detected":
                    issue_detected,

                "issue_category":
                    fallback[
                        "issue_category"
                    ],

                "issue_summary":
                    issue_summary,

                "severity":
                    severity,

                "sentiment":
                    sentiment,

                "warranty_related":
                    fallback[
                        "warranty_related"
                    ],

                "safety_issue":
                    fallback[
                        "safety_issue"
                    ],

                "repeat_issue":
                    False,

                "evidence":
                    call.get(
                        "evidence",
                        []
                    ),

                "transcript":
                    transcript,

                "raw_response":
                    call
            }

        except Exception as error:

            last_error = error

            if attempt_number == 0:
                time.sleep(3)

    raise RuntimeError(
        f"CALL-E live call failed: {last_error}"
    )


def simulate_call(
    repair,
    scenario="issue"
):

    if scenario == "healthy":

        return {
            "call_id":
                f"TEST-{repair.get('repair_id')}",

            "status":
                "completed",

            "task_completed":
                True,

            "issue_detected":
                False,

            "issue_category":
                "None",

            "issue_summary":
                "Customer confirmed the repaired device is working properly.",

            "severity":
                "Low",

            "sentiment":
                "Positive",

            "warranty_related":
                False,

            "safety_issue":
                False,

            "repeat_issue":
                False,

            "evidence":
                [],

            "transcript":
                []
        }

    if scenario == "critical":

        return {
            "call_id":
                f"TEST-{repair.get('repair_id')}",

            "status":
                "completed",

            "task_completed":
                True,

            "issue_detected":
                True,

            "issue_category":
                "Heating",

            "issue_summary":
                "Customer reports severe heating after repair.",

            "severity":
                "Critical",

            "sentiment":
                "Negative",

            "warranty_related":
                True,

            "safety_issue":
                True,

            "repeat_issue":
                False,

            "evidence":
                [],

            "transcript":
                []
        }

    return {
        "call_id":
            f"TEST-{repair.get('repair_id')}",

        "status":
            "completed",

        "task_completed":
            True,

        "issue_detected":
            True,

        "issue_category":
            "Screen",

        "issue_summary":
            "Customer reports screen touch freezing after repair.",

        "severity":
            "High",

        "sentiment":
            "Negative",

        "warranty_related":
            True,

        "safety_issue":
            False,

        "repeat_issue":
            False,

        "evidence":
            [],

        "transcript":
            []
    }


def make_followup_call(
    repair,
    test_mode=True,
    scenario="issue"
):

    if test_mode:

        return simulate_call(
            repair=repair,
            scenario=scenario
        )

    return make_live_followup_call(
        repair
    )