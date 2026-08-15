import os
from datetime import datetime

from dotenv import load_dotenv
from calle import CalleClient


load_dotenv()

CALLE_API_KEY = os.getenv("CALLE_API_KEY")


VERIFICATION_SCHEMA = {
    "type": "object",
    "required": [
        "issue_resolved",
        "customer_confirmed",
        "final_csat",
        "feedback"
    ],
    "properties": {
        "issue_resolved": {
            "type": "boolean"
        },

        "customer_confirmed": {
            "type": "boolean"
        },

        "final_csat": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5
        },

        "feedback": {
            "type": "string"
        }
    }
}


def normalize_phone(phone):

    phone = str(
        phone or ""
    ).strip()

    phone = (
        phone
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )

    if (
        phone.startswith("91")
        and not phone.startswith("+")
    ):
        phone = "+" + phone

    if not phone.startswith("+"):

        raise ValueError(
            "Phone number must be E.164 format, "
            "example +916386351022"
        )

    return phone


def build_verification_task(case):

    phone = normalize_phone(
        case.get("phone")
    )

    customer_name = case.get(
        "customer_name",
        "Customer"
    )

    device = case.get(
        "device",
        "device"
    )

    repair_type = case.get(
        "repair_type",
        "repair"
    )

    issue = case.get(
        "issue",
        "reported service issue"
    )

    resolution_type = case.get(
        "resolution_type",
        "technician recovery"
    )

    return f"""
Call {phone}.

You are AfterCare AI.

You are making a post-recovery verification call.

Customer:
{customer_name}

Device:
{device}

Original Repair:
{repair_type}

Original Issue:
{issue}

Recovery Action:
{resolution_type}

Start by saying:

"Hello {customer_name}, this is AfterCare AI.
I am following up regarding the issue you reported
after your recent {repair_type} for your {device}.
Our service team has worked on the issue,
and I would like to confirm whether it has now been resolved."

Ask:

"Is the original issue fully resolved now?"

Wait for the customer's answer.

If the customer says YES:

Ask:

"Great. On a scale of 1 to 5,
how satisfied are you with the final resolution,
where 1 is very dissatisfied and 5 is very satisfied?"

Capture the rating.

Then thank the customer and end politely.

If the customer says NO:

Ask:

"What issue are you still experiencing?"

Understand their response.

Then say:

"Thank you for letting me know.
I will reopen the case and share this
with our service team for further review."

Do not promise:
- refund
- replacement
- warranty approval
- free service

IMPORTANT:

issue_resolved must be true only if the customer
clearly confirms the original issue is fixed.

customer_confirmed must be true only when
the customer confirms resolution.

If the issue is not resolved,
customer_confirmed must be false.

If the customer does not provide a CSAT rating,
use 3 as the neutral fallback.

Base the result only on the actual conversation.
""".strip()


def extract_transcript(call):

    transcript = []

    for recipient in call.get(
        "recipients",
        []
    ):

        for attempt in recipient.get(
            "attempts",
            []
        ):

            transcript.extend(
                attempt.get(
                    "transcript_turns",
                    []
                )
            )

    return transcript


def extract_structured_result(call):

    for recipient in call.get(
        "recipients",
        []
    ):

        result = recipient.get(
            "structured_result"
        )

        if (
            isinstance(result, dict)
            and result
        ):
            return result

    result = call.get(
        "structured_result"
    )

    if (
        isinstance(result, dict)
        and result
    ):
        return result

    return {}


def customer_text(
    transcript
):

    lines = []

    for turn in transcript:

        speaker = str(
            turn.get(
                "speaker",
                ""
            )
        ).lower()

        text = str(
            turn.get(
                "text",
                ""
            )
        ).strip()

        if (
            speaker in [
                "user",
                "customer",
                "recipient"
            ]
            and text
        ):
            lines.append(text)

    return " ".join(lines).lower()


def fallback_analysis(
    transcript
):

    text = customer_text(
        transcript
    )

    if not text:

        raise RuntimeError(
            "No customer response captured."
        )

    unresolved_phrases = [
        "not resolved",
        "not fixed",
        "still issue",
        "still problem",
        "same issue",
        "same problem",
        "not working",
        "still not working",
        "problem remains"
    ]

    resolved_phrases = [
        "resolved",
        "fixed",
        "working fine",
        "working properly",
        "all good",
        "problem solved",
        "issue solved",
        "yes it is fine",
        "yes it's fine"
    ]

    unresolved = any(
        phrase in text
        for phrase in unresolved_phrases
    )

    resolved = any(
        phrase in text
        for phrase in resolved_phrases
    )

    if unresolved:

        issue_resolved = False

    elif resolved:

        issue_resolved = True

    else:

        issue_resolved = False

    csat = 3

    if any(
        x in text
        for x in [
            "five",
            "5 out of 5",
            "rating 5"
        ]
    ):
        csat = 5

    elif any(
        x in text
        for x in [
            "four",
            "4 out of 5",
            "rating 4"
        ]
    ):
        csat = 4

    elif any(
        x in text
        for x in [
            "two",
            "2 out of 5",
            "rating 2"
        ]
    ):
        csat = 2

    elif any(
        x in text
        for x in [
            "one",
            "1 out of 5",
            "rating 1"
        ]
    ):
        csat = 1

    if issue_resolved:

        feedback = (
            "Customer confirmed the original "
            "service issue is resolved."
        )

    else:

        feedback = (
            "Customer indicated that the original "
            "service issue is not fully resolved."
        )

    return {
        "issue_resolved":
            issue_resolved,

        "customer_confirmed":
            issue_resolved,

        "final_csat":
            csat,

        "feedback":
            feedback
    }


def make_live_verification_call(
    case
):

    if not CALLE_API_KEY:

        raise ValueError(
            "CALLE_API_KEY missing in .env"
        )

    client = CalleClient(
        api_key=CALLE_API_KEY
    )

    call = client.calls.create_and_wait(
        task=build_verification_task(
            case
        ),
        result_schema=
            VERIFICATION_SCHEMA
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
            f"CALL-E verification failed. "
            f"Status: {status}"
        )

    transcript = extract_transcript(
        call
    )

    if not transcript:

        raise RuntimeError(
            "Verification call completed "
            "but no transcript was captured."
        )

    result = extract_structured_result(
        call
    )

    fallback = fallback_analysis(
        transcript
    )

    if not result:
        result = fallback

    issue_resolved = result.get(
        "issue_resolved",
        fallback["issue_resolved"]
    )

    customer_confirmed = (
        result.get(
            "customer_confirmed",
            issue_resolved
        )
    )

    final_csat = result.get(
        "final_csat",
        fallback["final_csat"]
    )

    feedback = result.get(
        "feedback",
        fallback["feedback"]
    )

    try:
        final_csat = int(
            final_csat
        )

    except Exception:
        final_csat = 3

    final_csat = max(
        1,
        min(
            5,
            final_csat
        )
    )

    return {
        "call_id":
            call.get("id")
            or call.get(
                "call_id"
            ),

        "status":
            "completed",

        "completed_at":
            datetime.now().isoformat(),

        "issue_resolved":
            bool(
                issue_resolved
            ),

        "customer_confirmed":
            bool(
                customer_confirmed
            ),

        "final_csat":
            final_csat,

        "feedback":
            feedback,

        "transcript":
            transcript,

        "raw_response":
            call
    }