import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Loan Approval System", layout="wide")
st.title("🏦 Automated Loan Approval System")

st.write("Upload Loan Application Dataset (CSV or Excel)")

uploaded_file = st.file_uploader("Upload Dataset", type=["csv", "xlsx"])

REQUIRED_COLUMNS = [
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "CIBIL_Score"
]

if uploaded_file is not None:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip()

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Check required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
        st.stop()

    # Convert to numeric
    for col in REQUIRED_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=REQUIRED_COLUMNS)

    # 🔥 VECTORISED APPROVAL LOGIC (Fast & Professional)

    total_income = df["ApplicantIncome"] + df["CoapplicantIncome"]
    loan_ratio = df["LoanAmount"] / (total_income + 1)

    df["Loan_Status"] = np.where(
        (df["CIBIL_Score"] >= 750) & (loan_ratio < 0.5),
        "Approved",
        np.where(
            (df["CIBIL_Score"] >= 650) & (loan_ratio < 0.4),
            "Approved",
            "Not Approved"
        )
    )

    st.success("Loan decisions calculated automatically ✅")

    # Summary Metrics
    approved_count = (df["Loan_Status"] == "Approved").sum()
    rejected_count = (df["Loan_Status"] == "Not Approved").sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Approved", approved_count)
    col2.metric("Total Rejected", rejected_count)

    # Filter Option
    st.subheader("Filter Results")

    status_filter = st.selectbox(
        "Select Loan Status",
        ["All", "Approved", "Not Approved"]
    )

    if status_filter != "All":
        df = df[df["Loan_Status"] == status_filter]

    st.dataframe(df)

    # Optional: Download updated file
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Processed Dataset",
        csv,
        "processed_loan_results.csv",
        "text/csv"
    )

else:
    st.info("Please upload a dataset to start.")