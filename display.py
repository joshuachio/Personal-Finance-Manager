from cProfile import label
from tkinter.font import families
import streamlit as st
from parse import Year, Month
import datetime
import pandas as pd
import plotly.express as px
# from data_collection import Get

month_dict = {
    "January": '01',
    "February": '02',
    "March": '03',
    "April": '04',
    "May": '05',
    "June": '06',
    "July": '07',
    "August": '08',
    "September": '09',
    "October": '10',
    "November": '11',
    "December": '12'
}

st.set_page_config(
    page_title="Financial Budget",
    layout="centered"
)

st.title("Financial Budget")


def highlight(num):
    if num < -20:
        return 'color: #F04426'
    elif num > 40:
        return 'color: lightgreen'
    else:
        return 'color: white'

with st.sidebar:
    st.title("Select A Budget Period")
    select = st.selectbox("Yearly/Month Budget", ("None", "Yearly", "Monthly"))

if select == 'Yearly':
    with st.sidebar:
        year = st.selectbox("Choose a year", ("2022", "2023"))
    y = Year(year)
    st.subheader("Total Transactions for " + year)
    st.dataframe(y.budgetData.style.format({'amount': '{:.2f}'}).applymap(highlight, 'amount'), 800, 10000)
    st.subheader(year + ' ' + "Transactions Sorted by Category")
    st.dataframe(y.category_transactions.style.format({'amount': '{:.2f}'}).applymap(highlight, 'amount'), 800, 10000)
    st.subheader(year + ' ' + "Transactions Sorted by Price")
    st.dataframe(y.price_sort.style.format({'amount': '{:.2f}'}).applymap(highlight, 'amount'), 800, 10000)
elif select == 'Monthly':
    with st.sidebar:
        month = st.selectbox("Choose a mnoth", ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"))
        year = st.selectbox("Choose a year", ("2022", "2023"))
    m = Month(month_dict[month], year)
    st.subheader(month + ' Overview')
    c = pd.DataFrame([-m.total_debit, m.total_credit, m.net_gain], index=['Total Expenses', 'Total Income', 'Net Cash Flow'], columns=['Total ($)'])
    s = px.bar(
        c,
        labels={'index': 'Categories', 'value': '($)'},
        text_auto=True,
    )
    s.update_layout(
        font_family='Serif',
        font_size=14,
    )
    st.plotly_chart(s)
    st.subheader("Total Transactions for " + month + " " + year)
    st.dataframe(m.transactions_df.style.format({'amount': '{:.2f}'}).applymap(highlight, 'amount'), 800, 10000)
    st.subheader(month + " " + year + ' ' + "Transactions Sorted by Category")
    st.dataframe(m.category_transactions.style.format({'amount': '{:.2f}'}).applymap(highlight, 'amount'), 800, 10000)
    st.subheader(month + " " + year + ' ' + "Transactions Sorted by Price")
    st.dataframe(m.price_sort.style.format({'amount': '{:.2f}'}).applymap(highlight, 'amount'), 800, 10000)

