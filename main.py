import streamlit as st


st.set_page_config(
        page_title='Personal Project',
        page_icon='favicon'
    )

applications = {
    'Personal Expense Tracker': 'expense\\expense.py',
    'Simple Tax Calculator': 'tax_calculator\\tax.py'
}

# Dropdown menu to select the application
selected_app = st.selectbox('Select Application', list(applications.keys()))

# Import and run the selected application
exec(open(applications[selected_app]).read())