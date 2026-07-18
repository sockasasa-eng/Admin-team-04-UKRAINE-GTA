import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Адмін-бот", page_icon="⚖️")

# Читаємо повний текст правил з файлу
with open("rules.txt", "r", encoding="utf-8") as f:
    full_rules = f.read()

api_key = st.secrets["GEMINI_API_KEY"]
admin_password = st.secrets["ADMIN_PASSWORD"]

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Пароль:", type="password")
    if st.button("Увійти"):
        if password == admin_password:
            st.session_state.authenticated = True
            st.rerun()
else:
    st.title("Адмін-панель UKRAINE GTA")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Питання по правилах:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Бот тепер використовує повний текст з rules.txt
            query = f"Використовуючи ці правила:\n{full_rules}\n\nВідповідай на питання: {prompt}"
            response = model.generate_content(query)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
