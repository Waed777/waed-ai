import streamlit as st
import pandas as pd
from scraper import scrape_global_data
from ai_logic import generate_insights

st.set_page_config(page_title="🤖 Waed AI", layout="wide")

# Sidebar للغة
language = st.sidebar.radio("Language / اللغة", ["English", "العربية"])

# إعداد النصوص حسب اللغة
texts = {
    "English": {
        "title": "🤖 Waed AI – Big Data Intelligence Assistant",
        "instruction": "Ask Waed AI about global data:",
        "scrape_btn": "Start Scraping",
        "download_btn": "Download CSV",
        "sample_questions": ["Average price", "Highest price", "Get global book data"]
    },
    "العربية": {
        "title": "🤖 وعد AI – مساعد تحليلي للبيانات الضخمة",
        "instruction": "اطرح سؤالك على وعد AI:",
        "scrape_btn": "ابدأ الاستخراج",
        "download_btn": "تحميل CSV",
        "sample_questions": ["متوسط السعر", "أعلى سعر", "احصل على بيانات الكتب العالمية"]
    }
}

t = texts[language]

st.markdown(f"<h1 style='text-align:center;color:#6c63ff'>{t['title']}</h1>", unsafe_allow_html=True)
st.write(t["instruction"])

# Buttons for sample questions
st.write("💡 Sample Questions:")
cols = st.columns(len(t["sample_questions"]))
for i, q in enumerate(t["sample_questions"]):
    if cols[i].button(q):
        user_question = q
        st.session_state['user_question'] = user_question

# Input box if user wants to type
user_question = st.text_input("", value=st.session_state.get('user_question', ""))

if st.button(t["scrape_btn"]):
    data = scrape_global_data()
    df = pd.DataFrame(data)
    
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
