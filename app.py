import streamlit as st
from datetime import date
from db import init_db, add_transaction, fetch_filtered
from finance import calculate_emi

st.set_page_config(page_title="Credit & Debt Tracker")

init_db()

# -----------------------------
# NAVIGATION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    st.session_state.page = "home"

def go_credit():
    st.session_state.page = "credit"

def go_debt():
    st.session_state.page = "debt"

# =============================
# HOME PAGE
# =============================
if st.session_state.page == "home":
    st.title("Credit & Debt Tracker")

    st.subheader("Choose an option")

    col1, col2 = st.columns(2)

    with col1:
        st.button("💰 Credit", use_container_width=True, on_click=go_credit)

    with col2:
        st.button("💳 Debt", use_container_width=True, on_click=go_debt)

# =============================
# CREDIT PAGE
# =============================
elif st.session_state.page == "credit":
    st.title("💰 Credit")

    st.button("⬅ Back", on_click=go_home)

    with st.form("credit_form"):
        amount = st.number_input("Amount", min_value=0.0)
        note = st.text_input("Remark")
        submitted = st.form_submit_button("Add Credit")

        if submitted:
            add_transaction("credit", amount, 0, 1, note)
            st.success("Credit added")

    st.subheader("Credit History")

    c1, c2 = st.columns(2)
    with c1:
        start = st.date_input("From", date(2024, 1, 1))
    with c2:
        end = st.date_input("To", date.today())

    keyword = st.text_input("Search remark")

    credits = fetch_filtered(
        "credit",
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d"),
        keyword
    )

    for c in credits:
        st.write(f"₹{c[2]} | {c[5]} | {c[6]}")

# =============================
# DEBT PAGE
# =============================
elif st.session_state.page == "debt":
    st.title("💳 Debt")

    st.button("⬅ Back", on_click=go_home)

    with st.form("debt_form"):
        amount = st.number_input("Amount", min_value=0.0)
        interest = st.number_input("Annual Interest (%)", min_value=0.0)
        months = st.number_input("Duration (months)", min_value=1)
        note = st.text_input("Remark")
        submitted = st.form_submit_button("Add Debt")

        if submitted:
            add_transaction("debt", amount, interest, months, note)
            st.success("Debt added")

    st.subheader("Debt History")

    d1, d2 = st.columns(2)
    with d1:
        start = st.date_input("From", date(2024, 1, 1))
    with d2:
        end = st.date_input("To", date.today())

    keyword = st.text_input("Search remark")

    debts = fetch_filtered(
        "debt",
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d"),
        keyword
    )

    for d in debts:
        emi = calculate_emi(d[2], d[3], d[4])
        st.write(
            f"₹{d[2]} | {d[3]}% | {d[4]} months | EMI ₹{emi} | {d[5]} | {d[6]}"
        )
