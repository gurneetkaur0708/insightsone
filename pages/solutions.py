import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from prophet import Prophet
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Page config and title
st.set_page_config(page_title="BHEL AI Solutions", layout="wide")

page_bg_img = '''
<style>
.stApp {
  background-image: url("https://img.freepik.com/premium-photo/abstract-background-design-images-wallpaper-ai-generated_643360-164033.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Colors for dark futuristic theme
colors = {
    "background": "#0E1117",
    "text": "#7FDBFF",
    "bar": "#FF6F61",
    "pie": ["#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9"]
}

# Apply dark theme globally with CSS
st.markdown(f"""
    <style>
    .reportview-container {{
        background-color: {colors['background']};
        color: {colors['text']};
    }}
    .stButton>button {{
        background-color: {colors['bar']};
        color: white;
        border-radius: 12px;
        padding: 0.4em 1.5em;
        font-weight: 600;
    }}
    .streamlit-expanderHeader {{
        color: {colors['text']};
        font-weight: 600;
        font-size: 18px;
    }}
    .stMarkdown {{
        color: {colors['text']};
    }}
    /* Scrollbar style */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {colors['background']};
    }}
    ::-webkit-scrollbar-thumb {{
        background-color: {colors['bar']};
        border-radius: 20px;
        border: 2px solid {colors['background']};
    }}
    </style>
""", unsafe_allow_html=True)

# Header banner image (replace with your own image path or URL)
st.image("https://yourdubaiguide.com/wp-content/uploads/2021/04/BHEL-Logo-768x416.jpg", width=300 ,use_container_width=False)

st.title("🚀 BHEL AI Integration – Problem & Solutions")

# Sidebar with navigation/info
st.sidebar.header("About This Dashboard")
st.sidebar.write("""
This dashboard demonstrates AI-driven solutions and real-time demand prediction to help BHEL optimize energy use and improve operational efficiency.
- Explore AI solutions  
- Analyze demand prediction data interactively  
- Visualize insights with dynamic charts  
""")

# Problem statement
st.markdown("### 🔴 Problem Statement")
st.write("""
A smart AI dashboard for BHEL that showcases how AI can be integrated into core operations like prediction model, digital twins, and smart data analysis. The dashboard should include interactive visualizations, ML model outputs, and real-time insights, demonstrating the role of AI in improving decision-making, efficiency, and energy management.
""")

with st.expander("Solution 1: Digital Twin Analysis- Tata Elxsi"):
    st.markdown("** Analysis:**")
    st.markdown("""
-  Simulation-driven design, real-time monitoring, and predictive maintenance using IoT  
-  Cloud platforms integration (Azure, AWS) combined with AI/ML predictive models  
-  Advanced AR/VR visualization for immersive system analysis  
-  Time series analysis for trend and seasonality detection  
-  Extreme Learning Machines (ELM) for rapid demand prediction  
-  Grey Relation Analysis (GRA) for weighting influencing factors  
-  Real-time data integration for adaptive forecasting  
-  Scenario simulation to manage supply chain risks
""")

    st.markdown("** Impact:**")
    st.markdown("""
-  Execution time: 7–11 months  
-  Cost: ₹3 – ₹7 crore  
-  Achieved $11 million savings on coking coal procurement  
-  Estimated 9% reduction in overall procurement costs  
-  Efficiency gain: 10–25% reduction in material and operational costs  
-  93% prediction accuracy, outperforming traditional ARIMA models  
-  Enabled confident, risk-aware strategic buying decisions
""")

    st.image("images/qdtimage.png", width=400)

    with open("elxsifinal.docx", "rb") as file:
        st.download_button(" Download Full Report", data=file, file_name="elxsifinal.docx")

st.markdown("---")


with st.expander(" Solution 2: Predictive Maintenance for Rotating Equipment"):
    st.markdown("**Analysis:**")
    st.write("""
Client: NTPC (India’s largest power utility)

Tech Partner: TCS

Goal: Reduce unplanned downtime, increase turbine and motor lifespan

Tools/Tech: IoT sensors, Azure Cloud, ML models, thermal imaging, vibration monitoring 
    """)
    st.markdown("**Impact:**")
    st.write("""

 25–30% reduction in downtime

 Savings of over ₹50 crores/year

 Maintenance planning improved by 60%

 Predictive alerts reduced emergency breakdowns by 70%

 Implementation Time & Cost Estimates
Time: Approximately 4 to 6 months for full deployment, including sensor installation, AI model training, and dashboard setup.

Cost: Around ₹70 lakhs to ₹1 crore, covering sensors, cloud infrastructure, AI development, and training.

Benefit: This investment can significantly reduce downtime, cut maintenance costs, and improve equipment lifespan.
    """)
    st.image("images/pred.png", width=400)

    with open("qdt.docx", "rb") as file:
        st.download_button("📄 Download Full Report", data=file, file_name="Predictive_Maintenance_BHEL_Report.docx")


with st.expander(" Solution 3: Demand Prediction Model - Quantum Data Technology"):
    st.markdown("** Core Components:**")
    st.markdown("""
-  **Time Series Analysis**: Detects trends and seasonality in demand data.  
-  **Extreme Learning Machines (ELM)**: Enables rapid and efficient demand prediction.  
-  **Grey Relation Analysis (GRA)**: Weighs the influence of various predictive factors.  
-  **Real-time Data Integration**: Adapts predictions dynamically as new data streams in.  
-  **Scenario Simulation**: Assists in supply chain risk management and what-if analysis.
    """)

    st.markdown("**📈 Data Sources Integrated:**")
    st.markdown("""
- Historical raw material prices  
- Global market indicators  
- Supply chain disruptions  
- Internal production data
    """)

    st.markdown("**💡 Impact:**")
    st.markdown("""
-  Achieved **$11 million savings** on coking coal procurement.  
-  Realized an estimated **9% reduction** in overall procurement operation costs.  
-  **93% prediction accuracy**, outperforming traditional ARIMA models.  
-  Enabled confident, risk-aware strategic buying decisions.
    """)

    st.image("images/qdtimage.png", width=400)

    with open("qdt.docx", "rb") as file:
        st.download_button("📄 Download Full Report", data=file, file_name="qdt.docx")

st.markdown("---")


# Load demand prediction section
st.header(" Demand Prediction Dashboard")

st.title(" Upload Forecast CSV & Analyze Energy Demand")

uploaded_file = st.file_uploader("Upload a Prophet forecast CSV file", type=["csv"])

if uploaded_file:
    try:
        # ---------- Load and Preprocess ----------
        df = pd.read_csv(uploaded_file)

        # Check required column
        if 'yhat' not in df.columns or 'ds' not in df.columns:
            st.error("CSV must contain at least 'ds' (date) and 'yhat' (forecasted load) columns.")
            st.stop()

        df['ds'] = pd.to_datetime(df['ds'])

        # ---------- Simulated Region Split ----------
        regions = ['Region A', 'Region B', 'Region C', 'Region D']
        df['Region A'] = df['yhat'] * 0.4
        df['Region B'] = df['yhat'] * 0.3
        df['Region C'] = df['yhat'] * 0.2
        df['Region D'] = df['yhat'] * 0.1

        # ---------- Select Forecast Date ----------
        step = st.slider(
            "Select Prediction Date:",
            min_value=0,
            max_value=min(30, len(df) - 1),
            value=0,
            format="Day %d"
        )

        selected_date = df.iloc[step]['ds'].date()
        st.markdown(f"### 🔎 Predicted Demand for: **{selected_date}**")

        # ---------- Metrics ----------
        load_values = df.loc[step, regions]
        peak_load = load_values.max()
        avg_load = load_values.mean()
        total_load = df.loc[step, 'yhat']

        col1, col2, col3 = st.columns(3)
        col1.metric(" Total Load (units)", f"{total_load:.2f}")
        col2.metric(" Peak Region Load", f"{peak_load:.2f}")
        col3.metric(" Avg Region Load", f"{avg_load:.2f}")

        # ---------- Bar Chart ----------
        bar_fig = go.Figure(data=[
            go.Bar(
                x=regions,
                y=load_values,
                marker_color=colors["bar"],
                text=[f"{v:.1f}" for v in load_values],
                textposition='auto'
            )
        ])
        bar_fig.update_layout(
            title="Demand Prediction by Region",
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font_color=colors["text"],
            yaxis=dict(title="Load (units)")
        )

        # ---------- Pie Chart ----------
        pie_fig = go.Figure(data=[
            go.Pie(
                labels=regions,
                values=load_values,
                hole=0.4,
                marker_colors=colors["pie"],
                textinfo='label+percent',
            )
        ])
        pie_fig.update_layout(
            title="Demand Distribution",
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font_color=colors["text"]
        )

        # ---------- Show Charts ----------
        st.markdown("###  Visual Breakdown")
        col1, col2 = st.columns(2)
        col1.plotly_chart(bar_fig, use_container_width=True)
        col2.plotly_chart(pie_fig, use_container_width=True)

        # ---------- Optional: Show Full Table ----------
        with st.expander("🔎 Show Full Forecast Table"):
            st.dataframe(df[['ds', 'yhat'] + regions])

    except Exception as e:
        st.error(f" Error processing file: {e}")
else:
    st.info("Upload a CSV file generated by Prophet to see analysis.")

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Dashboard Title ---
st.title("📊 BHEL Financial Dashboard – FY 2024–25")

# --- KPIs Section ---
st.subheader("🔑 Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("🧾 FY Revenue", "₹27,350 Cr", "+19%")
col2.metric("💼 FY Profit Before Tax", "₹725 Cr", "+230%")
col3.metric("📈 Q4 Profit", "₹504 Cr", "+4%")

st.markdown("---")

# --- Quarterly Data Table ---
quarterly_data = {
    "Quarter": ["Q1", "Q2", "Q3", "Q4"],
    "Revenue (₹ Cr)": [5900, 6250, 7050, 9150],
    "Profit (₹ Cr)": [120, 180, 230, 504],
}
df = pd.DataFrame(quarterly_data)

# --- Revenue vs Profit Bar Chart ---
st.subheader("📊 Quarterly Revenue vs Profit")
fig1 = px.bar(
    df,
    x="Quarter",
    y=["Revenue (₹ Cr)", "Profit (₹ Cr)"],
    barmode="group",
    title="Revenue & Profit Per Quarter (₹ Cr)",
    labels={"value": "₹ Crore", "variable": "Metric"},
    text_auto=True
)
st.plotly_chart(fig1)

# --- Profit Trend Line Chart ---
st.subheader("📈 Profit Trend Over Quarters")
fig2 = px.line(
    df,
    x="Quarter",
    y="Profit (₹ Cr)",
    markers=True,
    title="Profit Growth (₹ Cr)",
    labels={"Profit (₹ Cr)": "Profit in ₹ Cr"}
)
st.plotly_chart(fig2)

# --- Pie Chart for Revenue Share by Units (Fictional) ---
st.subheader("🥧 Revenue Share by Unit (Sample)")
unit_data = {
    "Unit": ["Bhopal", "Haridwar", "Trichy", "Hyderabad", "Bangalore"],
    "Revenue": [4278, 3820, 5020, 3290, 3942]
}
unit_df = pd.DataFrame(unit_data)
fig3 = px.pie(
    unit_df,
    names="Unit",
    values="Revenue",
    title="Revenue Share by BHEL Units",
    hole=0.4
)
st.plotly_chart(fig3)

# --- Final Info Box ---
st.info("🔍 BHEL recorded a robust growth in FY 2024–25 with ₹27,350 Cr revenue and highest quarterly profit in 14 years (₹504 Cr in Q4).")
