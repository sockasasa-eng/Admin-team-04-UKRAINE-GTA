import streamlit as st
import google.generativeai as genai

# Конфігурація сторінки
st.set_page_config(page_title="Адмін-панель", page_icon="⚖️", layout="wide")

# CSS для імітації стилю гри (шрифти, фон, відступи)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    .main {
        background-color: #0e1117; /* Темний фон як у грі */
        color: white;
        font-family: 'Roboto', sans-serif;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #ffcc00; /* Золотистий акцент */
        font-weight: 700;
        text-transform: uppercase;
    }
    .stButton>button {
        background-color: #333;
        color: white;
        border: 1px solid #ffcc00;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Вставка емблеми (замініть посилання на ваше)
st.image("https://i.ibb.co/1YXMV5Ws/image.png", width=200) 

st.title("⚖️ Адміністративна панель")

if "GEMINI_API_KEY" not in st.secrets or "ADMIN_PASSWORD" not in st.secrets:
    st.error("Помилка: не знайдено ключі!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Ваш текст правил (залишається без змін)
game_rules = """Кортік свин!""" # Тут ваш великий текст правил

st.subheader("📋 Команди сервера")
st.text(game_rules[:500] + "...") # Для прикладу скорочено
