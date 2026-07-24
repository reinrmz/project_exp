import streamlit as st

from tax_calculator.tax import main as tax_main

st.set_page_config(
    page_title='Simple Tax Calculator',
    page_icon='favicon'
)

tax_main()
