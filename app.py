import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Адмін-бот", page_icon="⚖️")

# Перевірка наявності секретів
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Помилка: GEMINI_API_KEY не знайдено в налаштуваннях Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Завантаження правил з обробкою помилки, якщо файлу немає
try:
    with open("rules.txt", "r", encoding="utf-8") as f:
        full_rules = f.read()
except FileNotFoundError:
    full_rules = "Правила не завантажені."

model = genai.GenerativeModel('gemini-1.0-pro-latest')

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Пароль:", type="password")
    if st.button("Увійти"):
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Невірний пароль!")
else:
    st.title("Адмін-панель UKRAINE GTA")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Питання:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                query = f"Ти адміністратор UKRAINE GTA. Правила: {full_rules}\n\nПитання: {prompt}"
                response = model.generate_content(query)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Помилка ШІ: {e}")
