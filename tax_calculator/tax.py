import streamlit as st
import pandas as pd
import numpy as np

from constants import TAX_CALCULATOR
from utility import (
    inject_theme,
    render_masthead,
    render_about,
    section_label,
    render_hint,
    render_summary,
)

PERIOD_KEYS = ["period_1", "period_2", "period_3", "period_4"]


def period_lookup(x):
    return TAX_CALCULATOR.period_lkp[x]


def tax_table_generator(gdict):
    df = pd.DataFrame(gdict.items(), columns=['Period', 'Income'])
    df["Deductible"] = 250000

    df["Taxable"] = np.where(
        df["Period"] == 'period_1',
        df["Income"] - df["Deductible"],
        np.where(
            df["Period"] == 'period_2',
            df["Income"] + df["Income"].shift(1) - df["Deductible"],
            np.where(
                df["Period"] == 'period_3',
                df["Income"] + df["Income"].shift(1) + df["Income"].shift(2) - df["Deductible"],
                np.where(
                    df["Period"] == 'period_4',
                    df["Income"] + df["Income"].shift(1) + df["Income"].shift(2) + df["Income"].shift(3) - df["Deductible"],
                    0
                )
            )
        )
    )

    df["Taxable"] = np.where(
        df["Taxable"] <= 0,
        0,
        df["Taxable"]
    )

    df["Payable"] = np.where(
        df["Taxable"] > 0,
        np.where(
            df["Period"] == 'period_1',
            df["Taxable"] * 0.08,
            np.where(
                df["Period"] == 'period_2',
                (df["Taxable"]  * 0.08) - (df["Taxable"].shift(1) * 0.08),
                np.where(
                    df["Period"] == 'period_3',
                    (df["Taxable"]  * 0.08) - ((df["Taxable"].shift(1)  * 0.08) - (df["Taxable"].shift(2) * 0.08) + (df["Taxable"].shift(2)  * 0.08)),
                    np.where(
                        df["Period"] == 'period_4',
                        (df["Taxable"]  * 0.08) - ((df["Taxable"].shift(1)  * 0.08) - ((df["Taxable"].shift(2)  * 0.08) - (df["Taxable"].shift(3) * 0.08) + (df["Taxable"].shift(3)  * 0.08)) + ((df["Taxable"].shift(2)  * 0.08) - (df["Taxable"].shift(3) * 0.08)) + (df["Taxable"].shift(3) * 0.08)),
                        0
                    )
                )
            )
        ),
        0
    )

    df["Period"] = df["Period"].apply(period_lookup)

    return df


def _seed_income():
    """Return the starting Income per quarter, held in session state so edits
    persist across reruns."""
    if "income_by_period" not in st.session_state:
        st.session_state["income_by_period"] = {k: 0 for k in PERIOD_KEYS}
    return st.session_state["income_by_period"]


def main():
    inject_theme()
    render_masthead(TAX_CALCULATOR.app_version)

    income = _seed_income()

    # Compute the full table from the income held in session state.
    gross_dict = {k: income[k] for k in PERIOD_KEYS}
    df = tax_table_generator(gross_dict)

    render_about()

    # Single grid: Income is the only editable column; the computed columns
    # (Deductible / Taxable / Payable) are locked and repaint on each edit.
    section_label("Tax Ledger — enter income per quarter")
    render_hint(
        "Enter your gross income in the Income column for each quarter. "
        "The Deductible, Taxable, and Payable columns update automatically."
    )

    edited = st.data_editor(
        df[["Period", "Income", "Deductible", "Taxable", "Payable"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Period": st.column_config.TextColumn("Period", disabled=True),
            "Income": st.column_config.NumberColumn(
                "Income",
                help="Editable — type your gross income for each quarter.",
                min_value=0,
                step=10000,
                format="₱ %,.2f",
            ),
            "Deductible": st.column_config.NumberColumn(
                "Deductible", format="₱ %,.2f", disabled=True
            ),
            "Taxable": st.column_config.NumberColumn(
                "Taxable", format="₱ %,.2f", disabled=True
            ),
            "Payable": st.column_config.NumberColumn(
                "Payable", format="₱ %,.2f", disabled=True
            ),
        },
        key="tax_editor",
    )

    # Persist edited income; a change triggers a rerun that recomputes above.
    edited_income = [0 if pd.isna(v) else int(v) for v in edited["Income"]]
    new_income = dict(zip(PERIOD_KEYS, edited_income))
    if new_income != st.session_state["income_by_period"]:
        st.session_state["income_by_period"] = new_income
        st.rerun()

    total_payable = df["Payable"].sum()
    monthly_payable = total_payable / 12
    render_summary(total_payable, monthly_payable)


if __name__ == "__main__":
    main()
