import streamlit as st
import pandas as pd
import numpy as np

from constants import STATIC_TITLES

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

    return df

def main():
    st.set_page_config(
        page_title=STATIC_TITLES.page_title,
        page_icon='favicon'
    )
    st.title(STATIC_TITLES.page_title)

    # Variables
    gross_dict = dict()

    with st.container(border=True):
        st.subheader("Tax Table Calculator (8% Tax rate option)")
        for i in range(0, 4):
            gross_input = st.number_input(f"Input Gross for period {i+1}", min_value=0, step=10000, key=f"ginput_{i}")

            gross_dict[f"period_{i+1}"] = gross_input

        df = tax_table_generator(gross_dict)

        st.table(df)



if __name__ == "__main__":
    main()