import os
import pandas as pd

from datetime import datetime, timedelta

from services.scheduler import get_due_followups
from services.calle_service import make_followup_call
from services.ai_analysis import analyze_call_result

from services.risk_engine import (
    calculate_risk_score,
    classify_risk,
    get_recommended_action
)

from services.ticket_service import (
    create_ticket,
    get_priority,
    get_assigned_team
)

from services.resolution_service import (
    create_recovery_case
)

from services.customer_service import (
    update_customer_health
)


FOLLOWUPS_FILE = "data/followups.csv"
TICKETS_FILE = "data/tickets.csv"
RESOLUTIONS_FILE = "data/resolutions.csv"


def load_followups():

    if not os.path.exists(
        FOLLOWUPS_FILE
    ):
        return pd.DataFrame()

    try:

        return pd.read_csv(
            FOLLOWUPS_FILE
        )

    except pd.errors.EmptyDataError:

        return pd.DataFrame()


def save_followups(df):

    df.to_csv(
        FOLLOWUPS_FILE,
        index=False
    )


def get_existing_ticket(
    repair_id
):

    if not os.path.exists(
        TICKETS_FILE
    ):
        return None

    try:

        tickets_df = pd.read_csv(
            TICKETS_FILE
        )

    except pd.errors.EmptyDataError:

        return None

    if tickets_df.empty:
        return None

    match = tickets_df[
        tickets_df[
            "repair_id"
        ].astype(str)
        == str(repair_id)
    ]

    if match.empty:
        return None

    return (
        match.iloc[-1]
        .to_dict()
    )


def get_existing_recovery(
    ticket_id
):

    if not os.path.exists(
        RESOLUTIONS_FILE
    ):
        return None

    try:

        resolutions_df = pd.read_csv(
            RESOLUTIONS_FILE
        )

    except pd.errors.EmptyDataError:

        return None

    if resolutions_df.empty:
        return None

    match = resolutions_df[
        resolutions_df[
            "ticket_id"
        ].astype(str)
        == str(ticket_id)
    ]

    if match.empty:
        return None

    return (
        match.iloc[-1]
        .to_dict()
    )


def update_followup_record(
    repair_id,
    analysis,
    risk_score,
    recommended_action
):

    followups_df = load_followups()

    if followups_df.empty:
        return False

    mask = (
        followups_df[
            "repair_id"
        ].astype(str)
        == str(repair_id)
    )

    if not mask.any():
        return False

    if not analysis[
        "issue_detected"
    ]:

        health_status = "Healthy"

    elif analysis[
        "severity"
    ] == "Critical":

        health_status = "Critical"

    else:

        health_status = (
            "Issue Detected"
        )

    followups_df.loc[
        mask,
        "call_status"
    ] = "Completed"

    followups_df.loc[
        mask,
        "health_status"
    ] = health_status

    followups_df.loc[
        mask,
        "risk_score"
    ] = risk_score

    followups_df.loc[
        mask,
        "issue_detected"
    ] = (
        "Yes"
        if analysis[
            "issue_detected"
        ]
        else "No"
    )

    followups_df.loc[
        mask,
        "severity"
    ] = analysis[
        "severity"
    ]

    followups_df.loc[
        mask,
        "sentiment"
    ] = analysis[
        "sentiment"
    ]

    followups_df.loc[
        mask,
        "recommended_action"
    ] = recommended_action

    followups_df.loc[
        mask,
        "ticket_required"
    ] = (
        "Yes"
        if analysis[
            "ticket_required"
        ]
        else "No"
    )

    save_followups(
        followups_df
    )

    return health_status


def process_single_followup(
    repair,
    test_mode=True,
    scenario="issue"
):

    repair_id = repair[
        "repair_id"
    ]

    customer_name = repair[
        "customer_name"
    ]

    call_result = make_followup_call(
        repair=repair,
        test_mode=test_mode,
        scenario=scenario
    )

    analysis = analyze_call_result(
        call_result
    )

    risk_score = calculate_risk_score(
        issue_detected=analysis[
            "issue_detected"
        ],
        severity=analysis[
            "severity"
        ],
        sentiment=analysis[
            "sentiment"
        ],
        warranty_related=analysis[
            "warranty_related"
        ],
        safety_issue=analysis[
            "safety_issue"
        ],
        repeat_issue=analysis[
            "repeat_issue"
        ]
    )

    risk_level = classify_risk(
        risk_score
    )

    recommended_action = (
        get_recommended_action(
            score=risk_score,
            issue_detected=analysis[
                "issue_detected"
            ],
            safety_issue=analysis[
                "safety_issue"
            ],
            warranty_related=analysis[
                "warranty_related"
            ]
        )
    )

    health_status = (
        update_followup_record(
            repair_id=repair_id,
            analysis=analysis,
            risk_score=risk_score,
            recommended_action=
                recommended_action
        )
    )

    if not health_status:

        if not analysis[
            "issue_detected"
        ]:

            health_status = "Healthy"

        elif analysis[
            "severity"
        ] == "Critical":

            health_status = "Critical"

        else:

            health_status = (
                "Issue Detected"
            )

    update_customer_health(
        customer_name=
            customer_name,
        health_status=
            health_status,
        risk_score=
            risk_score,
        severity=
            analysis[
                "severity"
            ]
    )

    ticket = None
    recovery_case = None

    if analysis[
        "ticket_required"
    ]:

        existing_ticket = (
            get_existing_ticket(
                repair_id
            )
        )

        if existing_ticket:

            ticket = (
                existing_ticket
            )

        else:

            priority = (
                get_priority(
                    analysis[
                        "severity"
                    ]
                )
            )

            assigned_team = (
                get_assigned_team(
                    analysis[
                        "issue_category"
                    ],
                    analysis[
                        "severity"
                    ]
                )
            )

            warranty_review = (
                "Recommended"
                if analysis[
                    "warranty_related"
                ]
                else "Not Required"
            )

            ticket = create_ticket(
                repair_id=
                    repair_id,
                customer_name=
                    customer_name,
                issue=
                    analysis[
                        "issue_summary"
                    ],
                severity=
                    analysis[
                        "severity"
                    ],
                priority=
                    priority,
                assigned_team=
                    assigned_team,
                warranty_review=
                    warranty_review
            )

        if ticket:

            existing_recovery = (
                get_existing_recovery(
                    ticket[
                        "ticket_id"
                    ]
                )
            )

            if existing_recovery:

                recovery_case = (
                    existing_recovery
                )

            else:

                if analysis[
                    "severity"
                ] == "Critical":

                    delay_hours = 1

                elif analysis[
                    "severity"
                ] == "High":

                    delay_hours = 4

                else:

                    delay_hours = 8

                scheduled_for = (
                    datetime.now()
                    + timedelta(
                        hours=delay_hours
                    )
                ).strftime(
                    "%Y-%m-%d %H:%M"
                )

                recovery_case = (
                    create_recovery_case(
                        ticket_id=
                            ticket[
                                "ticket_id"
                            ],
                        customer_name=
                            customer_name,
                        resolution_type=
                            recommended_action,
                        assigned_to=
                            ticket[
                                "assigned_team"
                            ],
                        scheduled_for=
                            scheduled_for
                    )
                )

    return {
        "repair_id":
            repair_id,

        "customer_name":
            customer_name,

        "call_id":
            call_result.get(
                "call_id"
            ),

        "call_status":
            call_result.get(
                "status"
            ),

        "health_status":
            health_status,

        "issue_detected":
            analysis[
                "issue_detected"
            ],

        "issue_category":
            analysis[
                "issue_category"
            ],

        "issue_summary":
            analysis[
                "issue_summary"
            ],

        "severity":
            analysis[
                "severity"
            ],

        "sentiment":
            analysis[
                "sentiment"
            ],

        "warranty_related":
            analysis[
                "warranty_related"
            ],

        "safety_issue":
            analysis[
                "safety_issue"
            ],

        "risk_score":
            risk_score,

        "risk_level":
            risk_level,

        "recommended_action":
            recommended_action,

        "ticket":
            ticket,

        "recovery_case":
            recovery_case
    }


def process_due_followups(
    test_mode=True,
    scenario="issue"
):

    due_df = get_due_followups()

    if due_df.empty:
        return []

    followups_df = load_followups()

    processed_results = []

    for _, repair_row in (
        due_df.iterrows()
    ):

        repair = (
            repair_row.to_dict()
        )

        repair_id = repair[
            "repair_id"
        ]

        if not followups_df.empty:

            existing_completed = (
                followups_df[
                    (
                        followups_df[
                            "repair_id"
                        ].astype(str)
                        == str(
                            repair_id
                        )
                    )
                    &
                    (
                        followups_df[
                            "call_status"
                        ]
                        == "Completed"
                    )
                ]
            )

            if not (
                existing_completed.empty
            ):
                continue

        result = (
            process_single_followup(
                repair=repair,
                test_mode=test_mode,
                scenario=scenario
            )
        )

        processed_results.append(
            result
        )

        followups_df = (
            load_followups()
        )

    return processed_results