import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Адмін-бот", page_icon="⚖️")

if "GEMINI_API_KEY" not in st.secrets or "ADMIN_PASSWORD" not in st.secrets:
    st.error("Помилка: не знайдено ключі в Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ВИКОРИСТОВУЄМО ТІЛЬКИ ЦЮ ВЕРСІЮ, ВОНА НАЙСТАБІЛЬНІША
model = genai.GenerativeModel('gemini-1.5-flash-002')

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Пароль:", type="password")
    if st.button("Увійти"):
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.authenticated = True
            st.rerun()
else:
    st.title("Адмін-панель UKRAINE GTA")
    
    if prompt := st.chat_input("Питання:"):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Помилка ШІ: {e}")
