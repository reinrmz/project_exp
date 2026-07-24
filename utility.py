import streamlit as st


# --------------------------------------------------------------------------
# Theme / CSS
# --------------------------------------------------------------------------
def inject_theme():
    """Inject the ledger-terminal theme: fonts, palette, and component styling.

    Streamlit only exposes the DOM through injected CSS, so all of the
    fintech-dark styling lives here rather than in a stylesheet file.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --ink:      #0E1117;
            --surface:  #161B26;
            --hairline: #232A38;
            --text:     #E6E9EF;
            --muted:    #8B93A7;
            --amber:    #F5A524;
        }

        /* Tighten the default Streamlit page frame */
        .block-container {
            max-width: 760px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
        }
        #MainMenu, footer, header {visibility: hidden;}

        /* ---- Masthead ---------------------------------------------------- */
        .tc-masthead {
            border: 1px solid var(--hairline);
            border-radius: 14px;
            background:
                radial-gradient(120% 140% at 0% 0%, rgba(245,165,36,0.08), transparent 55%),
                var(--surface);
            padding: 1.6rem 1.8rem;
            margin-bottom: 1.5rem;
        }
        .tc-eyebrow {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--amber);
            margin: 0 0 0.4rem 0;
        }
        .tc-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1.9rem;
            line-height: 1.1;
            color: var(--text);
            margin: 0;
        }
        .tc-sub {
            font-size: 0.9rem;
            color: var(--muted);
            margin: 0.5rem 0 0 0;
        }

        /* ---- Section label ----------------------------------------------- */
        .tc-section {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--muted);
            margin: 1.6rem 0 0.6rem 0;
            padding-bottom: 0.4rem;
            border-bottom: 1px solid var(--hairline);
        }

        /* ---- Number inputs ----------------------------------------------- */
        div[data-testid="stNumberInput"] label p {
            font-size: 0.82rem !important;
            color: var(--muted) !important;
        }
        div[data-testid="stNumberInput"] input {
            font-family: 'JetBrains Mono', monospace !important;
            font-variant-numeric: tabular-nums;
        }

        /* ---- About expander ---------------------------------------------- */
        div[data-testid="stExpander"] details {
            border: 1px solid var(--hairline);
            border-radius: 10px;
            background: var(--surface);
        }
        div[data-testid="stExpander"] summary {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            letter-spacing: 0.06em;
            color: var(--muted);
        }
        div[data-testid="stExpander"] summary:hover {
            color: var(--amber);
        }

        /* ---- Usage hint --------------------------------------------------- */
        .tc-hint {
            border: 1px solid rgba(245,165,36,0.28);
            border-left: 3px solid var(--amber);
            border-radius: 8px;
            background: rgba(245,165,36,0.06);
            padding: 0.7rem 0.95rem;
            margin: 0.2rem 0 0.9rem 0;
            font-size: 0.85rem;
            line-height: 1.5;
            color: var(--muted);
        }
        .tc-hint-mark {
            color: var(--amber);
            margin-right: 0.5rem;
        }

        /* ---- Editable data grid ------------------------------------------ */
        /* Monospace, tabular figures inside the st.data_editor grid so the
           peso columns line up like a ledger. */
        div[data-testid="stDataFrame"] [role="gridcell"],
        div[data-testid="stDataEditor"] [role="gridcell"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-variant-numeric: tabular-nums;
        }
        div[data-testid="stDataFrame"] [role="columnheader"],
        div[data-testid="stDataEditor"] [role="columnheader"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.7rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--muted);
        }
        /* Flag the editable Income column (2nd column) with an amber header. */
        div[data-testid="stDataEditor"] [role="columnheader"][aria-colindex="2"] {
            color: var(--amber) !important;
            background: rgba(245, 165, 36, 0.10) !important;
            border-bottom: 2px solid var(--amber) !important;
        }

        /* ---- Payable summary cards ---------------------------------------- */
        .tc-cards {display: flex; gap: 1rem; margin-top: 1.5rem;}
        .tc-card {
            flex: 1;
            border: 1px solid var(--hairline);
            border-radius: 12px;
            background: var(--surface);
            padding: 1.1rem 1.2rem;
        }
        .tc-card.is-primary {
            border-color: rgba(245,165,36,0.45);
            background:
                linear-gradient(180deg, rgba(245,165,36,0.10), transparent 70%),
                var(--surface);
        }
        .tc-card-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--muted);
            margin: 0 0 0.5rem 0;
        }
        .tc-card-value {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            font-size: 1.6rem;
            line-height: 1;
            font-variant-numeric: tabular-nums;
            color: var(--text);
        }
        .tc-card.is-primary .tc-card-value {color: var(--amber);}

        @media (max-width: 640px) {
            .tc-cards {flex-direction: column;}
            .tc-title {font-size: 1.5rem;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# Render helpers
# --------------------------------------------------------------------------
def render_masthead(version):
    st.markdown(
        f"""
        <div class="tc-masthead">
            <p class="tc-eyebrow">BIR &middot; 8% Rate Option</p>
            <h1 class="tc-title">Quarterly Tax Ledger</h1>
            <p class="tc-sub">Enter your gross receipts per quarter to compute
            taxable income and tax payable. {version}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text):
    st.markdown(f'<p class="tc-section">{text}</p>', unsafe_allow_html=True)


def render_about():
    """Collapsible panel explaining who the calculator is for, plus the
    reminder that it does not file anything."""
    with st.expander("About this calculator", expanded=False):
        st.markdown(
            """
            **Who it's for** — Freelancers and self-employed professionals who
            have opted for the **8% income tax rate** and are **non-VAT
            registered**. The ₱250,000 deduction applies once against annual
            gross receipts.

            **Reminder** — Figures are estimates for planning only. Your actual
            liability depends on your BIR registration, other income, and
            allowable deductions.

            **Disclaimer** — This tool does **not** file anything. File your
            taxes through **eBIRForms** and submit accordingly.
            """
        )


def render_hint(text):
    st.markdown(
        f'<div class="tc-hint"><span class="tc-hint-mark">&#9998;</span>{text}</div>',
        unsafe_allow_html=True,
    )


def render_summary(total_payable, monthly_payable):
    st.markdown(
        f"""
        <div class="tc-cards">
            <div class="tc-card is-primary">
                <p class="tc-card-label">Total Tax Payable</p>
                <p class="tc-card-value">&#8369; {total_payable:,.2f}</p>
            </div>
            <div class="tc-card">
                <p class="tc-card-label">Monthly Equivalent</p>
                <p class="tc-card-value">&#8369; {monthly_payable:,.2f}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
