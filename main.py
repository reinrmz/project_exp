import streamlit as st
import pandas as pd
import numpy as np

from constants import STATIC_TITLES, STATIC_FORMATTING

def period_lookup(x):
    return STATIC_TITLES.period_lkp[x]

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

def call_subheader(text, header='h2'):
    st.markdown(f"<{header} style='text-align: center;'>{text}</{header}>", unsafe_allow_html=True)

def call_coloredtext(static_text, dynamic_text, dynamic_color='black', dynamic_font_size='16px'):

    static_part = f"<span style='font-size: 16px;'>{static_text}</span>"
    dynamic_part = (
        f"<span style='color: {dynamic_color}; font-size: {dynamic_font_size}; "
        f"text-decoration: underline;'>{dynamic_text}</span>"
    )

    space = "<span style='margin-left: 30px;'></span>"
    st.markdown(f"{static_part}{space}{dynamic_part}", unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title=STATIC_TITLES.page_title,
        page_icon='favicon'
    )
    st.title(STATIC_TITLES.page_title)

    # Variables
    gross_dict = dict()
    
    with st.container(border=True):
        call_subheader("Tax Table Calculator (8% Tax rate option)")

        for i in range(0, 4):
            period_txt = STATIC_TITLES.period_lkp[f"period_{i + 1}"]
            gross_input = st.number_input(f"Input Gross for {period_txt} period", min_value=0, step=10000, key=f"ginput_{i}")

            gross_dict[f"period_{i+1}"] = gross_input

        df = tax_table_generator(gross_dict)

        formatted_df = df.style.format(STATIC_FORMATTING.table_formatting)
        
        # Display Generated Tax Table
        call_subheader("Generated Tax Table",header='h4')
        st.table(formatted_df)

        total_payable = df["Payable"].sum()
        monthly_payable = total_payable / 12

        tp_formatted = f"₱ {total_payable:,.2f}"
        mp_formatted = f"₱ {monthly_payable:,.2f}"

        call_coloredtext(f"Your Total Tax Payable :", tp_formatted, dynamic_color="Red", dynamic_font_size='24px')

        call_coloredtext(f"Your Monthly Tax Payable :", mp_formatted, dynamic_color="Red", dynamic_font_size='24px')
        



if __name__ == "__main__":
    main()