import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Page Config
st.set_page_config(page_title="KAVACH Failure Dashboard", layout="wide")

# 1. Load Data
# Note: You can export your sheet as CSV or link via Google API
# For this example, replace 'data.csv' with your actual file path
@st.cache_data
def load_data():
    # Example structure based on your "FAILURE REPORT" tab
    df = pd.read_csv('your_kavach_data.csv') 
    df['Date'] = pd.to_datetime(df['Date'])
    return df

st.title("🚆 KAVACH Failure Analysis Dashboard")
st.markdown("Analysis of Locomotive and Radio failures [Source: KAVACH Report]")

# 2. Sidebar Filters
st.sidebar.header("Filter Data")
loco_filter = st.sidebar.multiselect("Select Loco No:", options=["37164", "30758", "37339", "39238"])

<<<<<<< HEAD
# 3. Key Metrics (Top Row)
col1, col2, col3 = st.columns(3)
col1.metric("Total Failures", "23") # Based on your current 23 entries 
col2.metric("Most Frequent Issue", "Radio Packet Loss")
col3.metric("Top Offender Loco", "37164")
=======
# Replace the text inside the quotes with your ACTUAL links from Step 1
import streamlit as st
import pandas as pd

# 1. Define the variable clearly at the top
SHEET_1_URL = "https://docs.google.com/spreadsheets/d/1imSFAMSxkEg63ix7n9h8v7mbObVbAZaY0X_0w3692G0/export?format=csv"

# ... other code ...

# 2. Now line 39 will work because the name exists!
current_url = SHEET_1_URL
>>>>>>> 9cb9d5e (Updating dashboard and adding requirements)

# 4. Visualizations
st.subheader("Failure Trends & Analysis")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("### Failures by Reason")
    # Mapping data from your "Reason of Failure" column 
    reasons = ["Radio Packet Loss", "RFID Damaged", "System Fault", "SOS Malfunction"]
    counts = [10, 5, 4, 4]
    fig, ax = plt.subplots()
    sns.barplot(x=counts, y=reasons, ax=ax, palette="viridis")
    st.pyplot(fig)

with chart_col2:
    st.write("### Failures per Section")
    # Based on your "Section (From-To)" column 
    sections = ["VR-ST", "ST-VR", "BL-ST", "DRD-GVD"]
    sec_counts = [8, 6, 4, 5]
    fig2, ax2 = plt.subplots()
    ax2.pie(sec_counts, labels=sections, autopct='%1.1f%%', startangle=140)
    st.pyplot(fig2)

# 5. Raw Data Inspection
st.subheader("Detailed Investigation Log")
st.write("Current focus: Intermittent communication and RFID issues ")
st.dataframe(pd.DataFrame({
    "Loco No": ["37164", "30823", "37111"],
    "Observation": ["Radio Packet Loss", "Investigation Required", "One Tag Missing"],
    "Action Taken": ["Waiting for shed", "Shed attention required", "Tag adjusted"]
}))
