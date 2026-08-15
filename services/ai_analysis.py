def get_customer_text(call_result):
    transcript = call_result.get("transcript", [])
    customer_lines = []

    for turn in transcript:
        speaker = str(turn.get("speaker", "")).lower()
        text = str(turn.get("text", "")).strip()

        if speaker in ["user", "customer", "recipient"] and text:
            customer_lines.append(text)

    return " ".join(customer_lines).lower()


def normalize_repair_type(repair_type):
    text = str(repair_type or "").lower()

    if any(x in text for x in ["screen", "display", "lcd", "touch"]):
        return "Display"

    if "battery" in text:
        return "Battery"

    if any(x in text for x in ["charging", "charger", "port"]):
        return "Charging"

    if "camera" in text:
        return "Camera"

    if any(x in text for x in ["speaker", "mic", "microphone", "audio"]):
        return "Audio"

    if any(x in text for x in ["water", "liquid"]):
        return "Water Damage"

    return "General"


def normalize_issue_category(category):
    text = str(category or "").lower().strip()

    if any(x in text for x in ["screen", "display", "touch", "lcd"]):
        return "Display / Touch"

    if any(x in text for x in ["heat", "smoke", "swelling", "safety"]):
        return "Heating / Safety"

    if "battery" in text:
        return "Battery"

    if any(x in text for x in ["charging", "charger", "port"]):
        return "Charging"

    if "camera" in text:
        return "Camera"

    if any(x in text for x in ["speaker", "microphone", "mic", "audio"]):
        return "Audio"

    if any(x in text for x in ["network", "wifi", "signal"]):
        return "Network"

    if any(x in text for x in ["performance", "slow", "freeze", "lag"]):
        return "Performance"

    return "Other"


def detect_issue(customer_text, issue_summary, structured_issue=False):
    text = f"{customer_text} {issue_summary}".lower()

    issue_phrases = [
        "not working",
        "doesn't work",
        "does not work",
        "problem",
        "issue",
        "freeze",
        "freezing",
        "hang",
        "hanging",
        "stuck",
        "broken",
        "not charging",
        "battery drain",
        "battery draining",
        "touch not working",
        "touch issue",
        "screen problem",
        "screen issue",
        "display issue",
        "flickering",
        "overheating",
        "heating",
        "very hot",
        "camera issue",
        "speaker issue",
        "microphone issue",
        "restart",
        "restarting",
        "same issue",
        "same problem",
        "still issue",
        "still problem"
    ]

    healthy_phrases = [
        "working fine",
        "working properly",
        "works fine",
        "works properly",
        "everything is fine",
        "all good",
        "no problem",
        "no issue",
        "perfectly fine",
        "fine now"
    ]

    if any(phrase in text for phrase in issue_phrases):
        return True

    if structured_issue:
        return True

    if any(phrase in text for phrase in healthy_phrases):
        return False

    return False


def detect_issue_category(
    customer_text,
    issue_summary,
    structured_category=""
):
    text = (
        f"{customer_text} "
        f"{issue_summary} "
        f"{structured_category}"
    ).lower()

    if any(
        x in text
        for x in [
            "smoke",
            "smoking",
            "battery swelling",
            "swollen battery",
            "swelling",
            "burning smell",
            "electrical smell",
            "fire",
            "spark",
            "sparking",
            "extremely hot",
            "very hot",
            "overheating"
        ]
    ):
        return "Heating / Safety"

    if any(
        x in text
        for x in [
            "screen",
            "display",
            "touch",
            "touchscreen",
            "lcd",
            "ghost touch",
            "flicker",
            "flickering"
        ]
    ):
        return "Display / Touch"

    if any(
        x in text
        for x in [
            "charging",
            "charger",
            "charging port",
            "not charging",
            "charge port"
        ]
    ):
        return "Charging"

    if any(
        x in text
        for x in [
            "battery",
            "battery drain",
            "draining",
            "battery backup"
        ]
    ):
        return "Battery"

    if any(
        x in text
        for x in [
            "camera",
            "camera lens",
            "camera focus"
        ]
    ):
        return "Camera"

    if any(
        x in text
        for x in [
            "speaker",
            "microphone",
            "mic",
            "sound",
            "audio",
            "earpiece"
        ]
    ):
        return "Audio"

    if any(
        x in text
        for x in [
            "network",
            "signal",
            "wifi",
            "wi-fi",
            "mobile data",
            "bluetooth"
        ]
    ):
        return "Network"

    if any(
        x in text
        for x in [
            "slow",
            "lag",
            "lagging",
            "restart",
            "restarting",
            "freeze",
            "freezing",
            "stuck"
        ]
    ):
        return "Performance"

    normalized = normalize_issue_category(
        structured_category
    )

    return normalized


def detect_safety_issue(
    customer_text,
    issue_summary
):
    text = f"{customer_text} {issue_summary}".lower()

    phrases = [
        "severe overheating",
        "extremely hot",
        "very hot",
        "too hot",
        "smoke",
        "smoking",
        "battery swelling",
        "battery swollen",
        "swollen battery",
        "burning smell",
        "electrical smell",
        "spark",
        "sparking",
        "fire",
        "explosion"
    ]

    return any(
        phrase in text
        for phrase in phrases
    )


def calculate_severity(
    customer_text,
    issue_summary,
    issue_detected,
    safety_issue,
    structured_severity="Low"
):
    text = f"{customer_text} {issue_summary}".lower()

    if not issue_detected:
        return "Low"

    if safety_issue:
        return "Critical"

    high_phrases = [
        "not working at all",
        "completely not working",
        "cannot use",
        "can't use",
        "totally unusable",
        "phone won't turn on",
        "phone does not turn on",
        "not charging at all",
        "keeps restarting",
        "continuously restarting",
        "touch completely not working",
        "screen completely not working"
    ]

    medium_phrases = [
        "sometimes",
        "intermittent",
        "occasionally",
        "freeze",
        "freezing",
        "flicker",
        "flickering",
        "battery drain",
        "slow charging",
        "touch issue",
        "screen issue",
        "stuck"
    ]

    if any(
        phrase in text
        for phrase in high_phrases
    ):
        return "High"

    if structured_severity in [
        "High",
        "Critical"
    ]:
        return structured_severity

    if any(
        phrase in text
        for phrase in medium_phrases
    ):
        return "Medium"

    return "Medium"


def determine_warranty_relation(
    repair_type,
    issue_category,
    customer_text,
    issue_summary,
    issue_detected
):
    if not issue_detected:
        return False

    text = f"{customer_text} {issue_summary}".lower()

    external_damage = [
        "dropped",
        "drop",
        "fell",
        "fall",
        "water exposure",
        "got wet",
        "liquid damage",
        "physical damage",
        "cracked again",
        "accident",
        "new damage"
    ]

    if any(
        phrase in text
        for phrase in external_damage
    ):
        return False

    repair_category = normalize_repair_type(
        repair_type
    )

    warranty_map = {
        "Display": [
            "Display / Touch",
            "Performance"
        ],
        "Battery": [
            "Battery",
            "Heating / Safety"
        ],
        "Charging": [
            "Charging",
            "Battery",
            "Heating / Safety"
        ],
        "Camera": [
            "Camera"
        ],
        "Audio": [
            "Audio"
        ],
        "Water Damage": [
            "Display / Touch",
            "Battery",
            "Charging",
            "Camera",
            "Audio",
            "Performance"
        ]
    }

    return issue_category in warranty_map.get(
        repair_category,
        []
    )


def detect_repeat_issue(
    customer_text,
    issue_summary,
    structured_repeat=False
):
    text = f"{customer_text} {issue_summary}".lower()

    phrases = [
        "same issue",
        "same problem",
        "again",
        "still happening",
        "still issue",
        "still problem",
        "problem returned",
        "issue returned"
    ]

    return (
        any(
            phrase in text
            for phrase in phrases
        )
        or bool(structured_repeat)
    )


def determine_sentiment(
    customer_text,
    issue_detected,
    structured_sentiment="Neutral"
):
    negative_phrases = [
        "angry",
        "frustrated",
        "disappointed",
        "very bad",
        "terrible",
        "worst",
        "not happy",
        "unhappy"
    ]

    positive_phrases = [
        "happy",
        "great",
        "perfect",
        "excellent",
        "working fine",
        "all good",
        "working properly"
    ]

    if any(
        phrase in customer_text
        for phrase in negative_phrases
    ):
        return "Negative"

    if any(
        phrase in customer_text
        for phrase in positive_phrases
    ):
        return "Positive"

    if structured_sentiment in [
        "Positive",
        "Negative"
    ]:
        return structured_sentiment

    if issue_detected:
        return "Negative"

    return "Neutral"


def analyze_call_result(
    call_result,
    repair=None
):
    if repair is None:
        repair = {}

    customer_text = get_customer_text(
        call_result
    )

    issue_summary = str(
        call_result.get(
            "issue_summary",
            ""
        )
    ).strip()

    structured_issue = bool(
        call_result.get(
            "issue_detected",
            False
        )
    )

    structured_category = str(
        call_result.get(
            "issue_category",
            ""
        )
    )

    issue_detected = detect_issue(
        customer_text,
        issue_summary,
        structured_issue
    )

    if not issue_detected:
        return {
            "issue_detected": False,
            "issue_category": "None",
            "issue_summary": (
                issue_summary
                if issue_summary
                else "Customer confirmed the repaired device is working properly."
            ),
            "severity": "Low",
            "sentiment": determine_sentiment(
                customer_text,
                False,
                call_result.get(
                    "sentiment",
                    "Neutral"
                )
            ),
            "warranty_related": False,
            "safety_issue": False,
            "repeat_issue": False,
            "ticket_required": False
        }

    issue_category = detect_issue_category(
        customer_text,
        issue_summary,
        structured_category
    )

    safety_issue = (
        detect_safety_issue(
            customer_text,
            issue_summary
        )
        or bool(
            call_result.get(
                "safety_issue",
                False
            )
        )
    )

    severity = calculate_severity(
        customer_text,
        issue_summary,
        True,
        safety_issue,
        call_result.get(
            "severity",
            "Low"
        )
    )

    repair_type = (
        repair.get(
            "repair_type"
        )
        or call_result.get(
            "repair_type"
        )
        or ""
    )

    warranty_related = determine_warranty_relation(
        repair_type,
        issue_category,
        customer_text,
        issue_summary,
        True
    )

    repeat_issue = detect_repeat_issue(
        customer_text,
        issue_summary,
        call_result.get(
            "repeat_issue",
            False
        )
    )

    sentiment = determine_sentiment(
        customer_text,
        True,
        call_result.get(
            "sentiment",
            "Neutral"
        )
    )

    if not issue_summary:
        issue_summary = (
            f"Customer reported a post-service "
            f"{issue_category.lower()} issue."
        )

    return {
        "issue_detected": True,
        "issue_category": issue_category,
        "issue_summary": issue_summary,
        "severity": severity,
        "sentiment": sentiment,
        "warranty_related": warranty_related,
        "safety_issue": safety_issue,
        "repeat_issue": repeat_issue,
        "ticket_required": True
    }