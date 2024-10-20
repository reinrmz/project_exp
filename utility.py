import streamlit as st
import pandas as pd
import numpy as np

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
