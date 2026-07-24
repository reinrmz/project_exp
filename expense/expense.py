import streamlit as st
import pandas as pd
import numpy as np

from constants import EXPENSE_TRACKER
from utility import call_subheader

@st.cache_data
def load_file(file, sheet_name):
    df = None
    if sheet_name != "None":
        df = pd.read_excel(file, sheet_name=sheet_name)
    else:
        st.warning("Please select a sheet.")

    return df

def cleanse_df(df):
    if df is not None:
        df = df.loc[~df["period"].isna()]
        df = df.fillna(0)
        return df

def main():
    with st.container(border=True):
        call_subheader("Personal Expense Tracker")
        source_file = st.file_uploader(f"Upload an Excel file for Analysis", type=["xlsx", "xls"])
        if source_file:
            excel_sheets = pd.ExcelFile(source_file).sheet_names
            excel_sheets.insert(0, "None")
            sheet_name = st.selectbox(f"Select Sheet to Analyze:", options=excel_sheets)

            source_df = load_file(source_file, sheet_name)
            cleansed_df = cleanse_df(source_df)
            if cleansed_df is not None:
                st.write(cleansed_df)

                # User input mapping
        else:
            st.warning("Please Upload File for Analysis first.")


if __name__ == "__main__":
    main()