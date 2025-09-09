import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Page setup
st.set_page_config(page_title="Fraud Checker", layout="centered")

# Set background image
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("cosmic-background-with-colorful-laser-lights-with-cool-shapes-perfect-digital-wallpaper (1).jpg")

# Title
st.title("🔍 Credit Card Fraud Detection Viewer")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("processed_data.csv")

df = load_data()

# Dropdown input for credit card numbers
cc_numbers = df['cc_num'].unique().tolist()
cc_input = st.selectbox("🔐 Select Credit Card Number", options=cc_numbers)

# Process input
if cc_input:
    filtered_df = df[df['cc_num'] == cc_input]

    if filtered_df.empty:
        st.warning("No data found for the selected credit card number.")
    else:
        st.subheader("🧾 All Transactions for this Credit Card")
        st.dataframe(filtered_df)

        # Count summary
        total_count = len(filtered_df)
        fraud_count = filtered_df['is_fraud'].sum()
        non_fraud_count = total_count - fraud_count

        st.markdown("---")
        st.markdown("### 📊 Transaction Summary")
        st.info(f"🔢 Total Transactions: **{total_count}**")
        st.error(f"🔴 Fraudulent Transactions: **{fraud_count}**")
        st.success(f"🟢 Non-Fraudulent Transactions: **{non_fraud_count}**")

        # Pie chart visualization
        st.markdown("### 📈 Fraud vs Non-Fraud Pie Chart")
        labels = ['Fraudulent', 'Non-Fraudulent']
        values = [fraud_count, non_fraud_count]
        colors = ['#ff4b4b', '#4caf50']

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, textprops={'fontsize': 12})
        ax.axis('equal')

        st.pyplot(fig)

        # Show fraud details
        fraud_df = filtered_df[filtered_df['is_fraud'] == 1]
        if not fraud_df.empty:
            st.subheader("🔴 Fraudulent Transactions")
            st.dataframe(fraud_df)

            def convert_df_to_excel(dataframe):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    dataframe.to_excel(writer, index=False, sheet_name='FraudData')
                output.seek(0)
                return output

            excel_data = convert_df_to_excel(fraud_df)

            st.download_button(
                label="📥 Download Fraud Details as Excel",
                data=excel_data,
                file_name=f"fraud_transactions_{cc_input}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.success("✅ No Fault Detected: All transactions are safe.")

