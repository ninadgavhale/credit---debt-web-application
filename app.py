import streamlit as st
from datetime import date
from db import init_db, add_transaction, fetch_history
from finance import calculate_emi

st.set_page_config(page_title="Credit & Debt Tracker")
init_db()

# -------------------------
# NAVIGATION STATE
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def nav(p):
    st.session_state.page = p

# =========================
# HOME
# =========================
if st.session_state.page == "home":
    st.title("Credit & Debt Tracker")

    st.subheader("Choose an option")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.button("💰 Credit", use_container_width=True, on_click=nav, args=("credit",))
    with c2:
        st.button("💳 Debit", use_container_width=True, on_click=nav, args=("debt",))
    with c3:
        st.button("📜 History", use_container_width=True, on_click=nav, args=("history",))

# =========================
# CREDIT
# =========================
elif st.session_state.page == "credit":
    st.title("💰 Credit")
    st.button("⬅ Back", on_click=nav, args=("home",))

    with st.form("credit_form"):
        amount = st.number_input("Amount", min_value=0.0)
        note = st.text_input("Remark")
        submit = st.form_submit_button("Add Credit")

        if submit:
            add_transaction("credit", amount, 0, 1, note)
            st.success("Credit added")

# =========================
# DEBIT
# =========================
elif st.session_state.page == "debt":
    st.title("💳 Debit")
    st.button("⬅ Back", on_click=nav, args=("home",))

    with st.form("debt_form"):
        amount = st.number_input("Amount", min_value=0.0)
        interest = st.number_input("Annual Interest (%)", min_value=0.0)
        months = st.number_input("Duration (months)", min_value=1)
        note = st.text_input("Remark")
        submit = st.form_submit_button("Add Debit")

        if submit:
            add_transaction("debt", amount, interest, months, note)
            st.success("Debit added")

# =========================
# HISTORY (PHONEPE STYLE)
# =========================
elif st.session_state.page == "history":
    st.title("📜 Transaction History")
    st.button("⬅ Back", on_click=nav, args=("home",))

    # ---- FILTER ROW (3 COLUMNS) ----
    f1, f2, f3 = st.columns(3)

    with f1:
        t_type = st.selectbox("Type", ["all", "credit", "debt"])

    with f2:
        start = st.date_input("From", date(2024, 1, 1))
        end = st.date_input("To", date.today())

    with f3:
        keyword = st.text_input("Remark keyword")

    # ---- FETCH & DISPLAY ----
    history = fetch_history(
        t_type,
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d"),
        keyword
    )

    st.divider()

    if not history:
        st.info("No transactions found")
    else:
        for h in history:
            _, typ, amount, interest, months, note, created = h

            if typ == "credit":
                st.write(f"🟢 ₹{amount} | Credit | {note} | {created}")
            else:
                emi = calculate_emi(amount, interest, months)
                st.write(
                    f"🔴 ₹{amount} | Debit | {interest}% | EMI ₹{emi} | {note} | {created}"
                )
