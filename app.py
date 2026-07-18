import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Діагностика API", page_icon="🔍")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    st.write("Список моделей, які бачить твій ключ:")
    
    try:
        # Цей цикл покаже нам реальні імена моделей
        for m in genai.list_models():
            st.write(f"Модель: {m.name} | Методи: {m.supported_generation_methods}")
    except Exception as e:
        st.error(f"Помилка при запиті списку: {e}")
else:
    st.error("Ключ не знайдено в Secrets")
