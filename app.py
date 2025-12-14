import streamlit as st
import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

st.set_page_config(page_title="Credit & Debt Tracker")
st.title("Credit & Debt Tracker")

data = load_data()

with st.form("entry_form"):
    entry_type = st.selectbox("Type", ["credit", "debt"])
    amount = st.number_input("Amount", min_value=0.0)
    note = st.text_input("Note")
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        data.append({
            "type": entry_type,
            "amount": amount,
            "note": note
        })
        save_data(data)
        st.success("Entry added")

credit = sum(e["amount"] for e in data if e["type"] == "credit")
debt = sum(e["amount"] for e in data if e["type"] == "debt")

st.subheader("Summary")
st.metric("Total Credit", f"₹{credit}")
st.metric("Total Debt", f"₹{debt}")
st.metric("Net Balance", f"₹{credit - debt}")

st.subheader("Entries")
for e in data:
    sign = "+" if e["type"] == "credit" else "-"
    st.write(f"{e['note']} : {sign}₹{e['amount']}")

