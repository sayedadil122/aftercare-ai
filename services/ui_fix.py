from textwrap import dedent
import streamlit as st


def apply_html_fix():

    # ---------------------------------------
    # HTML FIX
    # ---------------------------------------

    if not getattr(
        st,
        "_aftercare_html_patch",
        False
    ):

        original_markdown = st.markdown

        def fixed_markdown(
            body,
            *args,
            **kwargs
        ):

            unsafe_html = kwargs.get(
                "unsafe_allow_html",
                False
            )

            if (
                isinstance(body, str)
                and unsafe_html
            ):

                cleaned_html = dedent(
                    body
                ).strip()

                return st.html(
                    cleaned_html
                )

            return original_markdown(
                body,
                *args,
                **kwargs
            )

        st.markdown = fixed_markdown

        st._aftercare_html_patch = True


    # ---------------------------------------
    # GLOBAL UI
    # ---------------------------------------

    st.html(
        """
        <style>

        .stApp {
            background: #F5F7FB !important;
        }

        .block-container {
            max-width: 1450px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #101828 0%,
                    #172033 100%
                ) !important;
        }

        [data-testid="stSidebar"] * {
            color: white;
        }

        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #EAECF0;
            border-radius: 16px;
            padding: 14px 16px;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
        }

        button {
            border-radius: 12px !important;
        }

        </style>
        """
    )


    # ---------------------------------------
    # SIDEBAR
    # IMPORTANT:
    # Render on EVERY page rerun
    # ---------------------------------------

    with st.sidebar:

        st.html(
            """
            <div style="
                display:flex;
                align-items:center;
                gap:12px;
                padding:4px 0 14px 0;
            ">

                <div style="
                    width:42px;
                    height:42px;
                    border-radius:13px;
                    background:
                        linear-gradient(
                            135deg,
                            #7F56D9,
                            #6941C6
                        );
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:21px;
                ">
                    🤖
                </div>

                <div>

                    <div style="
                        font-size:20px;
                        font-weight:800;
                        color:white;
                    ">
                        AfterCare AI
                    </div>

                    <div style="
                        font-size:11px;
                        color:#98A2B3;
                    ">
                        Autonomous Service Recovery
                    </div>

                </div>

            </div>
            """
        )

        st.markdown("---")

        st.page_link(
            "app.py",
            label="Dashboard",
            icon="🏠"
        )

        st.page_link(
            "pages/new_service.py",
            label="New Service",
            icon="➕"
        )

        st.page_link(
            "pages/followups.py",
            label="Follow-up Calls",
            icon="📞"
        )

        st.page_link(
            "pages/issues.py",
            label="Issues",
            icon="⚠️"
        )

        st.page_link(
            "pages/tickets.py",
            label="Tickets",
            icon="🎫"
        )

        st.page_link(
            "pages/recovery_center.py",
            label="Recovery Center",
            icon="🛠️"
        )

        st.page_link(
            "pages/customers.py",
            label="Customers",
            icon="👥"
        )

        st.page_link(
            "pages/case_detail.py",
            label="Case Intelligence",
            icon="🧠"
        )

        st.page_link(
            "pages/insights.py",
            label="Insights",
            icon="📊"
        )

        st.page_link(
            "pages/settings.py",
            label="Settings",
            icon="⚙️"
        )

        st.markdown("---")

        st.success(
            "● Automation Online"
        )

        st.caption(
            "Simulation Mode"
        )