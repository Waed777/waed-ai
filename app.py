import streamlit as st
import pandas as pd
from scraper import scrape_global_data
from ai_logic import generate_insights

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(
    page_title="🤖 Waed AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Sidebar للغة
# -----------------------------
language = st.sidebar.radio("Language / اللغة", ["English", "العربية"])

# -----------------------------
# نصوص ثنائية اللغة
# -----------------------------
texts = {
    "English": {
        "title": "🤖 Waed AI – Big Data Intelligence Assistant",
        "instruction": "Ask Waed AI about global data or click a sample question:",
        "scrape_btn": "Start Scraping",
        "download_btn": "Download CSV",
        "sample_questions": [
            "Average price",
            "Highest price",
            "Get global book data"
        ],
        "no_data": "No data available to generate insights."
    },
    "العربية": {
        "title": "🤖 وعد AI – مساعد تحليلي للبيانات الضخمة",
        "instruction": "اطرح سؤالك على وعد AI أو اضغطي على أحد الأسئلة الجاهزة:",
        "scrape_btn": "ابدأ الاستخراج",
        "download_btn": "تحميل CSV",
        "sample_questions": [
            "متوسط السعر",
            "أعلى سعر",
            "احصل على بيانات الكتب العالمية"
        ],
        "no_data": "لا توجد بيانات لتحليلها."
    }
}

t = texts[language]

# -----------------------------
# واجهة جذابة مع Header
# -----------------------------
st.markdown(
    f"<h1 style='text-align:center; color:#6c63ff'>{t['title']}</h1>",
    unsafe_allow_html=True
)

st.write(t["instruction"])

# -----------------------------
# Buttons for Sample Questions
# -----------------------------
if 'user_question' not in st.session_state:
    st.session_state['user_question'] = ""

cols = st.columns(len(t["sample_questions"]))
for i, q in enumerate(t["sample_questions"]):
    if cols[i].button(q):
        st.session_state['user_question'] = q

# -----------------------------
# Input Box for User Question
# -----------------------------
user_question = st.text_input("", value=st.session_state['user_question'])

# -----------------------------
# Scraping and Display
# -----------------------------
if st.button(t["scrape_btn"]):
    try:
        data = scrape_global_data()
        if not data:
            st.warning(t["no_data"])
        df = pd.DataFrame(data)

        # -----------------------------
        # عرض الجدول مع تصميم
        # -----------------------------
        st.subheader("📊 Data Table" if language=="English" else "📊 جدول البيانات")
        st.dataframe(df.style.set_properties(**{
            'background-color': '#f0f2f6',
            'color': '#333',
            'border-color': '#6c63ff'
        }))

        # -----------------------------
        # Generate Smart Insights
        # -----------------------------
        insights = generate_insights(df, language)
        st.subheader("🧠 Waed AI Insight" if language=="English" else "🧠 استنتاج وعد AI")
        st.write(insights)

        # -----------------------------
        # CSV Download
        # -----------------------------
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=t["download_btn"],
            data=csv,
            file_name="waed_data.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
