import streamlit as st
from datetime import date
from db import init_db, add_transaction, fetch_all, fetch_filtered
from finance import calculate_emi
from strategy import snowball, avalanche

st.set_page_config(page_title="Credit & Debt Tracker")
st.title("Credit & Debt Tracker")

init_db()

# =========================
# ADD TRANSACTION FORM
# =========================
with st.form("entry_form"):
    t_type = st.selectbox("Type", ["credit", "debt"])
    amount = st.number_input("Amount", min_value=0.0)
    interest = st.number_input("Annual Interest (%)", min_value=0.0)
    months = st.number_input("Duration (months)", min_value=1)
    note = st.text_input("Remark")
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        add_transaction(t_type, amount, interest, months, note)
        st.success("Transaction added")

# =========================
# SUMMARY
# =========================
data = fetch_all()
total_credit = sum(r[2] for r in data if r[1] == "credit")
total_debt = sum(r[2] for r in data if r[1] == "debt")

st.subheader("Summary")
st.metric("Total Credit", f"₹{total_credit}")
st.metric("Total Debt", f"₹{total_debt}")
st.metric("Net Balance", f"₹{total_credit - total_debt}")

# =========================
# TABS (CREDIT / DEBT)
# =========================
tab_credit, tab_debt = st.tabs(["💰 Credit", "💳 Debt"])

# ---------- CREDIT TAB ----------
with tab_credit:
    st.subheader("Credit History")

    c1, c2 = st.columns(2)
    with c1:
        start = st.date_input("From", date(2024, 1, 1), key="c_from")
    with c2:
        end = st.date_input("To", date.today(), key="c_to")

    keyword = st.text_input("Remark keyword", key="c_kw")

    credits = fetch_filtered(
        "credit",
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d"),
        keyword
    )

    for c in credits:
        st.write(f"₹{c[2]} | {c[5]} | {c[6]}")

# ---------- DEBT TAB ----------
with tab_debt:
    st.subheader("Debt History")

    d1, d2 = st.columns(2)
    with d1:
        start = st.date_input("From", date(2024, 1, 1), key="d_from")
    with d2:
        end = st.date_input("To", date.today(), key="d_to")

    keyword = st.text_input("Remark keyword", key="d_kw")

    debts = fetch_filtered(
        "debt",
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d"),
        keyword
    )

    debt_objects = []

    for d in debts:
        emi = calculate_emi(d[2], d[3], d[4])
        st.write(
            f"₹{d[2]} | {d[3]}% | {d[4]} months | EMI ₹{emi} | {d[5]} | {d[6]}"
        )

        debt_objects.append({
            "amount": d[2],
            "interest": d[3],
            "months": d[4],
            "note": d[5]
        })

    st.subheader("Debt Payoff Strategy")

    strategy_choice = st.selectbox(
        "Choose strategy",
        ["Avalanche (Lowest Interest Cost)", "Snowball (Quick Wins)"]
    )

    ordered = avalanche(debt_objects) if "Avalanche" in strategy_choice else snowball(debt_objects)

    for i, d in enumerate(ordered, 1):
        st.write(f"{i}. {d['note']} | ₹{d['amount']} | {d['interest']}%")

