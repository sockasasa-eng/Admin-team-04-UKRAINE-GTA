import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Адмін-бот", page_icon="⚖️")

# Перевірка наявності секретів
if "GEMINI_API_KEY" not in st.secrets or "ADMIN_PASSWORD" not in st.secrets:
    st.error("Помилка: не знайдено GEMINI_API_KEY або ADMIN_PASSWORD у Secrets!")
    st.stop()

# Налаштування API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Використовуємо стабільну модель з твого списку
model = genai.GenerativeModel('models/gemini-3.5-flash')

# Логіка авторизації
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Введіть пароль:", type="password")
    if st.button("Увійти"):
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Невірний пароль!")
else:
    st.title("Адмін-панель UKRAINE GTA")
    
    # Історія чату
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Ввід повідомлень
    if prompt := st.chat_input("Питання до адміна:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Помилка ШІ: {e}")
