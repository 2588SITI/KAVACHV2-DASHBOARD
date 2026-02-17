import streamlit as st
import pandas as pd

import plotly.express as px

# Set page configuration
st.set_page_config(page_title="KAVACH Failure Analysis Dashboard", layout="wide")

# Title of the Dashboard
st.title("🛡️ KAVACH Failure Analysis Dashboard")

# 1. Load Data (Replace 'your_file.csv' with your exported CSV from Google Sheets)
@st.cache_data
def load_data():
    # Example data based on your Google Sheet 
    data = {
        'Date': ['2026-02-08', '2026-02-08', '2026-02-08', '2026-02-09', '2026-02-12', '2026-02-13', '2026-02-14', '2026-02-14', '2026-02-15'],
        'Train No.': [12935, 12936, 12925, 19011, 12925, 12925, 12925, 22959, 12922],
        'Loco No.': [37164, 37164, 37339, 37577, 30823, 39529, 37111, 39238, 30758],
        'Section': ['VR-ST', 'ST-VR', 'ST-VR', 'BL-ST', 'VR-ST', 'VR-ST', 'VR-ST', '-', 'ST-VR'],
        'Observation': [
            'Loco packets not received', 'Loco packets not received', 'Loco Packets not received',
            'Loco packets not received', 'Loco packets not received', 'Loco Packets not received',
            'One Tag Missing', 'Significant radio communication issues', 'Train stopped; SOS generated'
        ],
        'Reason': [
            'RFID damaged (Tag 695)', 'GVD Section Packets missed', 'Tag 577 removed',
            'Radio 2 failure', 'Investigation required', 'Packet loss Radio 1',
            'Foreign tags detected', 'Track Profile Not Read', 'No Network/SOS malfunction'
        ]
    }
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# 2. Sidebar Filters
st.sidebar.header("Filters")
selected_loco = st.sidebar.multiselect("Select Loco No.", options=df['Loco No.'].unique(), default=df['Loco No.'].unique())
filtered_df = df[df['Loco No.'].isin(selected_loco)]

# 3. Key Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Failures", len(filtered_df))
col2.metric("Unique Locos Affected", filtered_df['Loco No.'].nunique())
col3.metric("Most Frequent Train", filtered_df['Train No.'].mode()[0])

# 4. Visualizations
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    st.subheader("Failures Over Time")
    fig_date = px.histogram(filtered_df, x="Date", color="Loco No.", barmode="group", title="Trend of Observations")
    st.plotly_chart(fig_date, use_container_width=True)

with c2:
    st.subheader("Failures by Loco No.")
    fig_loco = px.pie(filtered_df, names="Loco No.", title="Loco Distribution")
    st.plotly_chart(fig_loco, use_container_width=True)

# 5. Data Table
st.subheader("Detailed Failure Logs")
st.dataframe(filtered_df, use_container_width=True)