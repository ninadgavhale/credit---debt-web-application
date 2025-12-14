import streamlit as st
from db import init_db, add_transaction, fetch_all

st.set_page_config(page_title="Credit & Debt Tracker")
st.title("Credit & Debt Tracker")

init_db()

with st.form("entry_form"):
    t_type = st.selectbox("Type", ["credit", "debt"])
    amount = st.number_input("Amount", min_value=0.0)
    interest = st.number_input("Annual Interest (%)", min_value=0.0)
    months = st.number_input("Duration (months)", min_value=1)
    note = st.text_input("Note")
    submitted = st.form_submit_button("Add")

    if submitted:
        add_transaction(t_type, amount, interest, months, note)
        st.success("Transaction added")

data = fetch_all()

credit = sum(r[2] for r in data if r[1] == "credit")
debt = sum(r[2] for r in data if r[1] == "debt")

st.subheader("Summary")
st.metric("Total Credit", f"₹{credit}")
st.metric("Total Debt", f"₹{debt}")
st.metric("Net Balance", f"₹{credit - debt}")
