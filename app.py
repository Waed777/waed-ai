import streamlit as st
import pandas as pd
from scraper import scrape_global_data
from ai_logic import generate_insights

st.set_page_config(page_title="🤖 Waed AI", layout="wide")

# Sidebar للغة
language = st.sidebar.radio("Language / اللغة", ["English", "العربية"])

texts = {
    "English": {
        "title": "🤖 Waed AI – Big Data Intelligence Assistant",
        "instruction": "Upload a CSV, scrape data, or ask a question:",
        "scrape_btn": "Start Scraping",
        "download_btn": "Download CSV",
        "upload_csv": "Upload CSV file",
        "sample_questions": ["Average price", "Highest price", "Get global book data"],
        "no_data": "No data available to generate insights."
    },
    "العربية": {
        "title": "🤖 وعد AI – مساعد تحليلي للبيانات الضخمة",
        "instruction": "ارفع CSV، استخرج بيانات، أو اطرح سؤال:",
        "scrape_btn": "ابدأ الاستخراج",
        "download_btn": "تحميل CSV",
        "upload_csv": "ارفع ملف CSV",
        "sample_questions": ["متوسط السعر", "أعلى سعر", "احصل على بيانات الكتب العالمية"],
        "no_data": "لا توجد بيانات لتحليلها."
    }
}

t = texts[language]

st.markdown(f"<h1 style='text-align:center; color:#6c63ff'>{t['title']}</h1>", unsafe_allow_html=True)
st.write(t["instruction"])

# -----------------------------
# Upload CSV
# -----------------------------
uploaded_file = st.file_uploader(t["upload_csv"], type=["csv"])
df = None
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

# -----------------------------
# Sample Questions Buttons
# -----------------------------
if 'user_question' not in st.session_state:
    st.session_state['user_question'] = ""

cols = st.columns(len(t["sample_questions"]))
for i, q in enumerate(t["sample_questions"]):
    if cols[i].button(q):
        st.session_state['user_question'] = q

user_question = st.text_input("", value=st.session_state['user_question'])

# -----------------------------
# Scrape Button
# -----------------------------
if st.button(t["scrape_btn"]):
    scraped_data = scrape_global_data()
    if scraped_data:
        scraped_df = pd.DataFrame(scraped_data)
        df = scraped_df if df is None else pd.concat([df, scraped_df], ignore_index=True)

# -----------------------------
# Display DataFrame and Insights
# -----------------------------
if df is not None:
    st.subheader("📊 Data Table" if language=="English" else "📊 جدول البيانات")
    st.dataframe(df)

    insights = generate_insights(df, language)
    st.subheader("🧠 Waed AI Insight" if language=="English" else "🧠 استنتاج وعد AI")
    st.write(insights)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=t["download_btn"],
        data=csv,
        file_name="waed_data.csv",
        mime="text/csv"
    )
else:
    st.info(t["no_data"])
