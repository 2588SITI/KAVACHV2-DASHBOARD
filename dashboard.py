import streamlit as st
import pandas as pd

import plotly.express as px

# Set page configuration
st.set_page_config(page_title="KAVACH Analysis TRO", layout="wide")

# Title
st.title("🛡️ KAVACH Failure Analysis Dashboard")

# --- DATA LOADING SECTION ---
# 1. Open your Google Sheet
# 2. File > Share > Publish to web
# 3. Select your Tab/Sheet, change 'Web Page' to 'CSV', and paste the links below:

# Replace the text inside the quotes with your ACTUAL links from Step 1
# Wrap it in quotes (single or double) and give it a name
sheet_url = "https://docs.google.com/spreadsheets/d/1imSFAMSxkEg63ix7n9h8v7mbObVbAZaY0X_0w3692G0/edit?usp=sharing"

@st.cache_data(ttl=300) # Refreshes every 5 minutes
def load_live_data(url):
    try:
        df = pd.read_csv(url)
        # Ensure 'Date' is handled correctly if it exists
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# --- SIDEBAR NAVIGATION ---
st.sidebar.header("Data Settings")
data_choice = st.sidebar.radio("Select Report Tab:", ["Failure Report", "New Analysis Sheet"])

# Load the chosen data
if data_choice == "Failure Report":
    current_url = SHEET_1_URL
else:
    current_url = SHEET_2_URL

df = load_live_data(current_url)

# --- DASHBOARD LOGIC ---
if not df.empty:
    # Sidebar Filters
    st.sidebar.markdown("---")
    st.sidebar.header("Filters")
    
    # Check if 'Loco No.' exists in the current sheet to prevent errors
    if 'Loco No.' in df.columns:
        selected_loco = st.sidebar.multiselect(
            "Select Loco No.", 
            options=df['Loco No.'].unique(), 
            default=df['Loco No.'].unique()
        )
        filtered_df = df[df['Loco No.'].isin(selected_loco)]
    else:
        filtered_df = df

    # 3. Key Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Entries", len(filtered_df))
    
    if 'Loco No.' in df.columns:
        m2.metric("Unique Locos", filtered_df['Loco No.'].nunique())
    
    if 'Reason' in df.columns:
        top_reason = filtered_df['Reason'].mode()[0] if not filtered_df['Reason'].empty else "N/A"
        m3.metric("Primary Reason", top_reason)

    # 4. Visualizations
    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        if 'Date' in filtered_df.columns:
            st.subheader("Trend Over Time")
            fig_date = px.histogram(filtered_df, x="Date", title="Log Frequency")
            st.plotly_chart(fig_date, use_container_width=True)
        else:
            st.info("No 'Date' column found in this sheet for trending.")

    with c2:
        if 'Reason' in filtered_df.columns:
            st.subheader("Failure Distribution")
            fig_reason = px.bar(filtered_df['Reason'].value_counts(), title="Top Failure Reasons")
            st.plotly_chart(fig_reason, use_container_width=True)
        else:
            st.info("No 'Reason' column found for distribution.")

    # 5. Data Table
    st.subheader("Raw Data View")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("Please paste your 'Publish to Web' CSV URLs into the code to see your Google Sheet data.")
