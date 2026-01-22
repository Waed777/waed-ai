import streamlit as st
import pandas as pd
from scraper import scrape_global_data
from ai_logic import generate_insights

# إعداد الصفحة
st.set_page_config(
    page_title="Waed AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar للغة
language = st.sidebar.radio("Language / اللغة", ["English", "العربية"])

# العناوين حسب اللغة
if language == "English":
    title = "🤖 Waed AI – Big Data Intelligence Assistant"
    instruction = "Ask Waed AI about global data:"
    scrape_btn = "Start Scraping"
    download_btn = "Download CSV"
else:
    title = "🤖 وعد AI – مساعد تحليلي للبيانات الضخمة"
    instruction = "اطرح سؤالك على وعد AI:"
    scrape_btn = "ابدأ الاستخراج"
    download_btn = "تحميل CSV"

st.title(title)
user_question = st.text_input(instruction)

if st.button(scrape_btn):
    data = scrape_global_data()
    df = pd.DataFrame(data)

    st.subheader("📊 Data Table" if language=="English" else "📊 جدول البيانات")
    st.dataframe(df)

    insights = generate_insights(df, language)
    st.subheader("🧠 Waed AI Insight" if language=="English" else "🧠 استنتاج وعد AI")
    st.write(insights)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=download_btn,
        data=csv,
        file_name="waed_data.csv",
        mime="text/csv"
    )
