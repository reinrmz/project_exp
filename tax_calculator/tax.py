import streamlit as st
import pandas as pd
import numpy as np

from constants import TAX_CALCULATOR, GENERAL_FORMATTING
from utility import call_coloredtext, call_subheader

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

def main():

    # Variables
    gross_dict = dict()
    
    with st.container(border=True):
        call_subheader("Tax Table Calculator (8% Tax rate option)")

        for i in range(0, 4):
            period_txt = TAX_CALCULATOR.period_lkp[f"period_{i + 1}"]
            gross_input = st.number_input(f"Input Gross for {period_txt} period", min_value=0, step=10000, key=f"ginput_{i}")

            gross_dict[f"period_{i+1}"] = gross_input

        df = tax_table_generator(gross_dict)

        formatted_df = df.style.format(TAX_CALCULATOR.table_formatting)
        
        # Display Generated Tax Table
        call_subheader("Generated Tax Table",header='h4')
        st.table(formatted_df)

        total_payable = df["Payable"].sum()
        monthly_payable = total_payable / 12

        tp_formatted = f"{GENERAL_FORMATTING.peso_format} {total_payable:,.2f}"
        mp_formatted = f"{GENERAL_FORMATTING.peso_format} {monthly_payable:,.2f}"

        call_coloredtext(f"Your Total Tax Payable :", tp_formatted, dynamic_color="Red", dynamic_font_size='24px')

        call_coloredtext(f"Your Monthly Tax Payable :", mp_formatted, dynamic_color="Red", dynamic_font_size='24px')
        



if __name__ == "__main__":
    main()