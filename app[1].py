import streamlit as st
import pandas as pd
from datetime import datetime
from database import save_transaction, db_status
from ml_model import predict_health_risk
from rag_engine import retrieve_answer

st.set_page_config(page_title="Family Health Wallet Copilot", page_icon="🏥", layout="wide")

# Sidebar
st.sidebar.title("🏥 Health Wallet Navigation")
page = st.sidebar.radio("Go to", ["Dashboard & Health Cards", "Prepaid Wallet & Transactions", "Health Claim Risk Predictor", "Policy RAG Assistant"])

st.sidebar.markdown("---")
is_db_connected = db_status()
st.sidebar.caption(f"Database Status: {'🟢 Connected' if is_db_connected else '🔴 Demo Mode (In-Memory)'}")

# Sample Data Initializer
if 'family_df' not in st.session_state:
    st.session_state.family_df = pd.DataFrame([
        {"Member ID": "FHW101", "Name": "Sundaram", "Relation": "Father", "Age": 62, "Health Card": "ACTIVE", "Wallet Balance (₹)": 15000},
        {"Member ID": "FHW102", "Name": "Lakshmi", "Relation": "Mother", "Age": 58, "Health Card": "ACTIVE", "Wallet Balance (₹)": 15000},
        {"Member ID": "FHW103", "Name": "Ramkumar", "Relation": "Self", "Age": 27, "Health Card": "ACTIVE", "Wallet Balance (₹)": 20000},
        {"Member ID": "FHW104", "Name": "Priya", "Relation": "Sister", "Age": 24, "Health Card": "ACTIVE", "Wallet Balance (₹)": 12000}
    ])

if 'transactions' not in st.session_state:
    st.session_state.transactions = [
        {"Date": "2026-10-15", "Member ID": "FHW101", "Type": "Expense", "Amount (₹)": 2500, "Description": "Apollo Pharmacy Medicines"},
        {"Date": "2026-10-20", "Member ID": "FHW103", "Type": "Recharge", "Amount (₹)": 10000, "Description": "Monthly Health Deposit"},
    ]

# PAGE 1: Dashboard & Health Cards
if page == "Dashboard & Health Cards":
    st.title("💳 Family Health Wallet & Dynamic Health Cards")
    st.markdown("Centralized family healthcare management dashboard.")
    
    total_balance = st.session_state.family_df["Wallet Balance (₹)"].sum()
    active_cards = len(st.session_state.family_df[st.session_state.family_df["Health Card"] == "ACTIVE"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Family Pooled Balance", f"₹{total_balance:,}")
    col2.metric("Total Registered Members", len(st.session_state.family_df))
    col3.metric("Active Health Cards", active_cards)
    
    st.subheader("👨‍👩‍👧‍👦 Family Member Profiles & Health Cards")
    st.dataframe(st.session_state.family_df, use_container_width=True)
    
    st.subheader("🆔 Dynamic Health Card Generator")
    selected_member = st.selectbox("Select Member to View Dynamic Health Card:", st.session_state.family_df["Name"])
    member_data = st.session_state.family_df[st.session_state.family_df["Name"] == selected_member].iloc[0]
    
    with st.container():
        st.markdown(f"""
        <div style="border:2px solid #2E7D32; border-radius:12px; padding:20px; background-color:#F1F8E9;">
            <h3 style="color:#1B5E20; margin-top:0;">🏥 FAMILY HEALTH CARD</h3>
            <p><b>Member Name:</b> {member_data['Name']} ({member_data['Relation']})</p>
            <p><b>Card ID:</b> {member_data['Member ID']}</p>
            <p><b>Age:</b> {member_data['Age']} years</p>
            <p><b>Available Balance:</b> ₹{member_data['Wallet Balance (₹)']:,}</p>
            <p><b>Status:</b> <span style="color:green; font-weight:bold;">{member_data['Health Card']}</span></p>
        </div>
        """, unsafe_allow_html=True)

# PAGE 2: Wallet & Transactions
elif page == "Prepaid Wallet & Transactions":
    st.title("💰 Prepaid Health Wallet & Transactions")
    
    tab1, tab2 = st.tabs(["Add Transaction / Recharge", "Transaction History"])
    
    with tab1:
        st.subheader("Record Health Expense or Top-Up Wallet")
        with st.form("txn_form"):
            m_id = st.selectbox("Select Member ID", st.session_state.family_df["Member ID"])
            t_type = st.selectbox("Transaction Type", ["Expense", "Recharge"])
            amt = st.number_input("Amount (₹)", min_value=100, step=500)
            desc = st.text_input("Description / Hospital Name", "Diagnostic Lab Test")
            submitted = st.form_submit_button("Submit Transaction")
            
            if submitted:
                new_txn = {
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Member ID": m_id,
                    "Type": t_type,
                    "Amount (₹)": amt,
                    "Description": desc
                }
                st.session_state.transactions.append(new_txn)
                
                # Update Session Balance
                idx = st.session_state.family_df.index[st.session_state.family_df["Member ID"] == m_id].tolist()[0]
                if t_type == "Recharge":
                    st.session_state.family_df.at[idx, "Wallet Balance (₹)"] += amt
                else:
                    st.session_state.family_df.at[idx, "Wallet Balance (₹)"] -= amt
                    
                save_transaction(m_id, t_type, amt, desc)
                st.success(f"Transaction of ₹{amt} successfully recorded for {m_id}!")

    with tab2:
        st.subheader("Recent Wallet Transactions")
        st.dataframe(pd.DataFrame(st.session_state.transactions), use_container_width=True)

# PAGE 3: Health Claim Risk Predictor
elif page == "Health Claim Risk Predictor":
    st.title("🤖 ML Health Claim Risk & Expense Predictor")
    st.markdown("Predict likelihood of high medical claims or emergency hospitalization risk based on health profile.")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Member Age", 1, 100, 55)
        claims = st.number_input("Prior Claims / Hospitalizations (Past 2 Yrs)", 0, 10, 2)
    with col2:
        avg_exp = st.number_input("Average Annual Medical Expense (₹)", 1000, 200000, 30000, step=5000)
        chronic = st.checkbox("Existing Chronic Condition (Diabetes, Hypertension, etc.)", value=True)
        
    if st.button("Predict Claim Risk Status"):
        pred, prob = predict_health_risk(age, claims, avg_exp, chronic)
        st.markdown("---")
        if pred == 1:
            st.error(f"⚠️ **High Medical Claim Risk Detected** (Probability: {prob*100:.1f}%)")
            st.info("💡 Recommendation: Keep adequate liquid funds in Prepaid Health Wallet and review emergency hospital network coverage.")
        else:
            st.success(f"✅ **Low / Normal Medical Claim Risk** (Probability of High Claim: {prob*100:.1f}%)")
            st.info("💡 Recommendation: Standard wallet reserve is sufficient.")

# PAGE 4: Policy RAG Assistant
elif page == "Policy RAG Assistant":
    st.title("💬 Health Wallet & Policy RAG Assistant")
    st.markdown("Ask any question regarding dynamic health cards, wallet top-ups, coverage, and hospital claims.")
    
    user_query = st.text_input("Enter your query:", "How does the Dynamic Health Card work?")
    if st.button("Search Knowledge Base") or user_query:
        ans, score = retrieve_answer(user_query)
        st.markdown("---")
        st.markdown(f"**Answer:** {ans}")
        st.caption(f"Confidence Similarity Score: {score}")
