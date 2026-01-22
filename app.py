import streamlit as st
import pandas as pd
from scraper import scrape_global_data
from ai_logic import generate_insights
import openai

# إعداد Streamlit
st.set_page_config(page_title="🤖 Waed AI", layout="wide")

# Sidebar للغة
language = st.sidebar.radio("Language / اللغة", ["English", "العربية"])

texts = {
    "English": {
        "title": "🤖 Waed AI – Smart Data & AI Assistant",
        "instruction": "Upload a CSV, scrape data, or ask any question:",
        "scrape_btn": "Start Scraping",
        "download_btn": "Download CSV",
        "upload_csv": "Upload CSV file",
        "sample_questions": ["Average price", "Highest price", "Give me insights"],
        "no_data": "No data available to generate insights."
    },
    "العربية": {
        "title": "🤖 وعد AI – مساعد ذكي للبيانات",
        "instruction": "ارفع CSV، استخرج بيانات، أو اطرح أي سؤال:",
        "scrape_btn": "ابدأ الاستخراج",
        "download_btn": "تحميل CSV",
        "upload_csv": "ارفع ملف CSV",
        "sample_questions": ["متوسط السعر", "أعلى سعر", "اعطني استنتاجات"],
        "no_data": "لا توجد بيانات لتحليلها."
    }
}

t = texts[language]

# Header
st.markdown(f"<h1 style='text-align:center; color:#6c63ff'>{t['title']}</h1>", unsafe_allow_html=True)
st.write(t["instruction"])

# Upload CSV
uploaded_file = st.file_uploader(t["upload_csv"], type=["csv"])
df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)

# Sample Questions Buttons
if 'user_question' not in st.session_state:
    st.session_state['user_question'] = ""

cols = st.columns(len(t["sample_questions"]))
for i, q in enumerate(t["sample_questions"]):
    if cols[i].button(q):
        st.session_state['user_question'] = q

user_question = st.text_input("", value=st.session_state['user_question'])

# Scraping Data
if st.button(t["scrape_btn"]):
    scraped_data = scrape_global_data()
    if scraped_data:
        scraped_df = pd.DataFrame(scraped_data)
        df = scraped_df if df is None else pd.concat([df, scraped_df], ignore_index=True)

# -----------------------------
# ChatGPT Integration for Smart Answers
# -----------------------------
def ask_chatgpt(question, df=None):
    """
    Send question + optional data summary to ChatGPT API
    """
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    
    prompt = "You are a data analyst AI. "
    if df is not None:
        prompt += f"Here is the data:\n{df.head(10).to_string()}\n"
    prompt += f"Answer the following question concisely: {question}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=300
    )
    return response['choices'][0]['message']['content']

# Display Data & Insights
if df is not None or user_question:
    if df is not None:
        st.subheader("📊 Data Table" if language=="English" else "📊 جدول البيانات")
        st.dataframe(df)

    # AI Insight
    if user_question:
        try:
            answer = ask_chatgpt(user_question, df)
            st.subheader("🧠 Waed AI Insight" if language=="English" else "🧠 استنتاج وعد AI")
            st.write(answer)
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

    # CSV Download
    if df is not None:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=t["download_btn"],
            data=csv,
            file_name="waed_data.csv",
            mime="text/csv"
        )
else:
    st.info(t["no_data"])

