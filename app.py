import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Loan Approval ML System", layout="wide")
st.title("🏦 Loan Approval Prediction System (ML Based)")

st.write("Step 1: Upload Training Dataset (Must contain Loan_Status column)")

# ------------------------
# TRAINING DATA UPLOAD
# ------------------------

train_file = st.file_uploader("Upload Training Dataset", type=["csv", "xlsx"], key="train")

if train_file is not None:

    if train_file.name.endswith(".csv"):
        train_df = pd.read_csv(train_file)
    else:
        train_df = pd.read_excel(train_file)

    train_df.columns = train_df.columns.str.strip()

    if "Loan_Status" not in train_df.columns:
        st.error("Training dataset must contain 'Loan_Status' column.")
        st.stop()

    st.subheader("Training Data Preview")
    st.dataframe(train_df.head())

    # Encode categorical columns
    df_model = train_df.copy()
    label_encoders = {}

    for col in df_model.columns:
        if df_model[col].dtype == "object":
            le = LabelEncoder()
            df_model[col] = le.fit_transform(df_model[col])
            label_encoders[col] = le

    X = df_model.drop("Loan_Status", axis=1)
    y = df_model["Loan_Status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    st.success(f"Model Trained Successfully ✅ | Accuracy: {round(acc*100,2)}%")

    # ------------------------
    # PREDICTION DATA UPLOAD
    # ------------------------

    st.write("Step 2: Upload New Dataset for Prediction (NO Loan_Status column)")

    predict_file = st.file_uploader("Upload Prediction Dataset", type=["csv", "xlsx"], key="predict")

    if predict_file is not None:

        if predict_file.name.endswith(".csv"):
            predict_df = pd.read_csv(predict_file)
        else:
            predict_df = pd.read_excel(predict_file)

        predict_df.columns = predict_df.columns.str.strip()

        st.subheader("Prediction Data Preview")
        st.dataframe(predict_df.head())

        # Apply same encoding
        predict_model_df = predict_df.copy()

        for col in predict_model_df.columns:
            if col in label_encoders:
                le = label_encoders[col]
                predict_model_df[col] = le.transform(predict_model_df[col])

        # Ensure same columns order
        predict_model_df = predict_model_df[X.columns]

        predictions = model.predict(predict_model_df)

        # Convert back to original labels
        if "Loan_Status" in label_encoders:
            predictions = label_encoders["Loan_Status"].inverse_transform(predictions)

        predict_df["Predicted_Loan_Status"] = predictions

        st.success("Predictions Generated Successfully ✅")
        st.dataframe(predict_df)

        # Download option
        csv = predict_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Prediction Results",
            csv,
            "loan_predictions.csv",
            "text/csv"
        )