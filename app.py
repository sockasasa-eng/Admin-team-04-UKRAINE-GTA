import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Адмін-панель", page_icon="⚖️")

if "GEMINI_API_KEY" not in st.secrets or "ADMIN_PASSWORD" not in st.secrets:
    st.error("Помилка: не знайдено ключі!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Використовуємо іншу модель, можливо, на ній є ліміт
model = genai.GenerativeModel('models/gemini-flash-latest')

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Пароль:", type="password")
    if st.button("Увійти"):
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

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
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Помилка 429 (Ліміт): Спробуй зачекати хвилину або модель заблокована. Деталі: {e}")
