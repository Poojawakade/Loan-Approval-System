import streamlit as st
import pandas as pd

st.set_page_config(page_title="Loan Approval System", layout="wide")

st.title("🏦 Intelligent Loan Approval System")

st.write("Upload Loan Application Dataset (CSV or Excel)")

uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])

# Approval Logic Function
def calculate_loan_status(row):
    total_income = row["ApplicantIncome"] + row["CoapplicantIncome"]
    loan_to_income_ratio = row["LoanAmount"] / (total_income + 1)

    # Bank Logic
    if row["CIBIL_Score"] >= 750 and loan_to_income_ratio < 0.5:
        return "Approved"
    elif row["CIBIL_Score"] >= 650 and loan_to_income_ratio < 0.4:
        return "Approved"
    else:
        return "Not Approved"

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Apply synthetic approval logic
    df["Loan_Status"] = df.apply(calculate_loan_status, axis=1)

    st.subheader("Loan Decision Results")
    st.dataframe(df)

    st.subheader("Filter Results")

    status_filter = st.selectbox(
        "Select Loan Status",
        ["All", "Approved", "Not Approved"]
    )

    if status_filter != "All":
        filtered_df = df[df["Loan_Status"] == status_filter]
        st.dataframe(filtered_df)

    st.subheader("🔍 Manual Loan Prediction")

    col1, col2 = st.columns(2)

    with col1:
        applicant_income = st.number_input("Applicant Income", value=5000)
        coapplicant_income = st.number_input("Coapplicant Income", value=0)
        loan_amount = st.number_input("Loan Amount (in thousands)", value=200)

    with col2:
        cibil_score = st.number_input("CIBIL Score (300-900)", value=700)
        loan_term = st.selectbox("Loan Term (months)", [180, 240, 300, 360])

    if st.button("Predict Loan Approval"):

        total_income = applicant_income + coapplicant_income
        loan_ratio = loan_amount / (total_income + 1)

        if cibil_score >= 750 and loan_ratio < 0.5:
            result = "Approved"
        elif cibil_score >= 650 and loan_ratio < 0.4:
            result = "Approved"
        else:
            result = "Not Approved"

        st.success(f"Loan Decision: {result}")

else:
    st.info("Please upload a dataset to proceed.")