import streamlit as st
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()
BACKEND_URL = str(os.getenv("BACKEND_URL"))

st.set_page_config(page_title="Data Preprocessing Agent", layout="centered")

st.title("📊 Data Preprocessing Agent")
st.write("Upload a CSV or Excel file, let the backend preprocess it, and download the cleaned version.")

# File upload
uploaded_file = st.file_uploader("Upload your file", type=["csv", "xls", "xlsx"])

if uploaded_file is not None:
    st.success(f"File `{uploaded_file.name}` uploaded successfully ✅")

    if st.button("Preprocess File"):
        with st.spinner("Processing..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            
            try:
                response = requests.post(f"{BACKEND_URL}/preprocess", files=files)

                if response.status_code == 200:
                    # Create a download button for the processed CSV
                    processed_csv = response.content
                    st.download_button(
                        label="⬇️ Download Processed File",
                        data=processed_csv,
                        file_name="processed.csv",
                        mime="text/csv"
                    )

                    # Optional: Preview the first few rows
                    df_preview = pd.read_csv(BytesIO(processed_csv))
                    st.subheader("🔍 Preview of Processed Data")
                    st.dataframe(df_preview.head())
                else:
                    st.error(f"Backend error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Request failed: {e}")
