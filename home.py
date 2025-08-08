import streamlit as st

# ---- Page Config ----
st.set_page_config(
    page_title="InsightsOne",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- Background Image Styling ----
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/premium-photo/abstract-background-design-images-wallpaper-ai-generated_643360-164033.jpg");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }
    .main-title {
        font-family: 'Trebuchet MS', sans-serif;
        font-size: 72px;
        font-weight: bold;
        background: linear-gradient(90deg, #f7f7f7, #dcdcdc);  /* Beige-White Gradient */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 60px;
    }
    .subtitle {
        font-family: 'Segoe UI', sans-serif;
        font-size: 26px;
        color: #f5f5dc; /* Light Beige */
        text-align: center;
        margin-bottom: 50px;
    }
    </style>

    <div class="main-title">InsightsOne</div>
    <div class="subtitle">One tool for all insights</div>
    """,
    unsafe_allow_html=True
)
# ---- CSS Styling ----
st.markdown("""
    <style>
    body {
        background-color: #0f0f0f;
    }
    .main {
        background-color: #0f0f0f;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        font-size: 60px;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #4e5ef9, #c34dbb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 24px;
        color: #cccccc;
        text-align: center;
        margin-bottom: 30px;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 40px;
    }
    .stButton > button {
        font-size: 16px;
        padding: 12px 24px;
        border-radius: 10px;
        background-color: #1f56ff;
        color: white;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #3f76ff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style='text-align: center;'>
        <img src="https://media.istockphoto.com/id/1473211827/photo/concept-of-ai-and-computer-technology.jpg?b=1&s=170667a&w=0&k=20&c=D66F_QIkg8ET5-QNJfzkxHlbhZQSxAJbhGEdrAPN5uM=" width="500">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    .tagline-list {
        font-family: 'Segoe UI', sans-serif;
        font-size: 20px;
        color: #e0e0d1;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 40px;
        line-height: 1.8;
        list-style-type: disc;
        display: inline-block;
        padding-left: 20px;
    }
    .tagline-container {
        display: flex;
        justify-content: center;
    }
    </style>

    <div class="tagline-container">
        <ul class="tagline-list">
            <li>Compare responses from 3 leading LLMs</li>
            <li>Upload CSV or Excel files for detailed data insights</li>
            <li>Discover AI-powered solutions tailored for BHEL</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# ---- Buttons Centered Below GIF ----
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button(" Chat with CompareBot"):
        st.switch_page("pages/app.py")

with col2:
    if st.button("Upload Files for Analysis"):
        st.switch_page("pages/BHEL_Mode.py")

with col3:
    if st.button("AI Solutions for BHEL"):
        st.switch_page("pages/solutions.py")

