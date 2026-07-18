import streamlit as st
import google.generativeai as genai

# Налаштування сторінки
st.set_page_config(page_title="Адмін-панель", page_icon="⚖️")

# Перевірка наявності ключів
if "GEMINI_API_KEY" not in st.secrets or "ADMIN_PASSWORD" not in st.secrets:
    st.error("Помилка: не знайдено ключі в Secrets!")
    st.stop()

# Підключення до API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Системна інструкція - вона змушує бота бути адміном гри
system_instruction = """
Ти - офіційний адміністратор проєкту UKRAINE GTA. 
Твоя задача - допомагати гравцям та відповідати на питання, що стосуються виключно гри UKRAINE GTA. 
Якщо питання не стосується гри, ввічливо відмовся відповідати. 
Не обговорюй політику, війну або інші теми, що не пов'язані з грою. 
Пиши чітко, коротко і зрозуміло.
"""

# Використання моделі з системною інструкцією для швидкості та фокусу
model = genai.GenerativeModel(
    model_name='models/gemini-2.0-flash',
    system_instruction=system_instruction
)

# Логіка авторизації
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Вхід в адмін-панель")
    password = st.text_input("Введіть пароль:", type="password")
    if st.button("Увійти"):
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Невірний пароль!")
    st.stop()

# Чат-інтерфейс
st.title("Адмін-панель UKRAINE GTA")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Питання до адміна:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Генерація відповіді
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Адмін мовчить...")
        except Exception as e:
            st.error(f"Помилка ШІ: {e}")
