import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import pydeck as pdk



# Gemini API setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="BHEL AI Mode", layout="wide")
st.title("🔍 BHEL AI File Analyzer & Q&A")

# Background
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

uploaded_file = st.file_uploader("📁 Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Load the file
    ext = uploaded_file.name.split(".")[-1].lower()
    if ext == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Show full data in expander
    with st.expander("🔍 View Full Dataset"):
        st.dataframe(df)

    # ---------------------- BASIC STATS ---------------------- #
    st.subheader("📊 Full Dataset Summary")
    st.write(f"**Number of Rows:** {df.shape[0]}")
    st.write(f"**Number of Columns:** {df.shape[1]}")

    st.write("**🧾 Columns & Data Types:**")
    st.dataframe(pd.DataFrame(df.dtypes, columns=["Data Type"]))

    st.write("**❗ Missing Values per Column:**")
    st.dataframe(pd.DataFrame(df.isnull().sum(), columns=["Missing Values"]))

    missing_percent = pd.DataFrame(
        (df.isnull().sum() / df.shape[0]) * 100, columns=["% Missing"]
    )
    st.write("**🧮 Percentage Missing:**")
    st.dataframe(missing_percent)

    st.write("**📐 Statistics for Numeric Columns:**")
    st.dataframe(df.describe())

    # Categorical column summary
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    if len(cat_cols) > 0:
        st.write("**🗂️ Summary for Categorical Columns:**")
        cat_summary = {}
        for col in cat_cols:
            unique_vals = df[col].nunique(dropna=True)
            top_val = df[col].mode(dropna=True).iloc[0] if not df[col].mode().empty else "N/A"
            cat_summary[col] = {
                "Unique Values": unique_vals,
                "Top Value": top_val,
            }
        cat_summary_df = pd.DataFrame(cat_summary).T
        st.dataframe(cat_summary_df)
    else:
        st.write("✅ No categorical columns detected.")

    # ---------------------- AI SUMMARY ---------------------- #
    st.subheader("📌 Overall AI Summary of Your Dataset")

    if st.button("Generate AI Summary"):
        with st.spinner("Analyzing data with Gemini..."):
            try:
                sample_data = df.head(50).to_string(index=False)

                gemini_prompt = (
                    f"You are a data scientist assistant. Here's a sample of the dataset:\n\n"
                    f"{sample_data}\n\n"
                    f"Please summarize the overall structure and insights from this dataset. "
                    f"Include observations about the data types, missing data, common patterns, "
                    f"and suggest potential next steps like data cleaning or analysis ideas."
                )

                model = genai.TextGenerationModel.from_pretrained("gemini-2.5-flash")
                summary_response = model.generate(
                    prompt=gemini_prompt,
                    max_output_tokens=700,
                    temperature=0.4,
                    top_p=0.9,
                )

                st.markdown("### 🧠 Gemini's Summary:")
                st.write(summary_response.text.strip())

            except Exception as e:
                st.error(f"Error generating summary: {e}")

    # ---------------------- CUSTOM Q&A ---------------------- #
    st.subheader("💬 Ask a question about your data")

    user_question = st.text_input("Type your question here:")

    if st.button("Get Answer from Gemini") and user_question.strip():
        with st.spinner("Getting answer from Gemini..."):
            try:
                sample_data = df.head(50).to_string(index=False)

                prompt = (
                    f"You are a helpful analyst. Based on the following dataset sample:\n\n"
                    f"{sample_data}\n\n"
                    f"Answer this user question clearly:\n{user_question}"
                )

                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(
    prompt,
    max_output_tokens=500,
    temperature=0.3,
    top_p=0.8,
)


                st.subheader("🧠 Gemini's Answer:")
                st.write(response.text.strip())

            except Exception as e:
                st.error(f"Error querying Gemini API: {e}")

else:
    st.info("📤 Upload a CSV or Excel file to begin analysis and Q&A.")


