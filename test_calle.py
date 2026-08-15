import os

from dotenv import load_dotenv
from calle import CalleClient


load_dotenv()


api_key = os.getenv(
    "CALLE_API_KEY"
)

if not api_key:
    raise ValueError(
        "CALLE_API_KEY missing in .env"
    )


client = CalleClient(
    api_key=api_key
)


print(
    "Starting CALL-E live test..."
)


call = client.calls.create_and_wait(
    task=(
        "Call +916386351022 and ask: "
        "Hello, this is AfterCare AI. "
        "Can you hear me clearly? "
        "Wait for the person's answer before ending the call."
    ),
    result_schema={
        "type": "object",
        "required": [
            "can_hear_clearly"
        ],
        "properties": {
            "can_hear_clearly": {
                "type": "string",
                "enum": [
                    "yes",
                    "no",
                    "unknown"
                ]
            }
        }
    }
)


print(
    "\nCALL STATUS:"
)

print(
    call.get(
        "status"
    )
)


print(
    "\nSTRUCTURED RESULT:"
)

print(
    call.get(
        "structured_result"
    )
)


print(
    "\nEVIDENCE:"
)

print(
    call.get(
        "evidence"
    )
)


print(
    "\nFULL RESPONSE:"
)

print(
    call
)