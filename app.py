import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Адмін-бот", page_icon="⚖️")

# Налаштування ключа
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    # Автоматичний пошук моделі
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Вибираємо першу доступну модель
        if available_models:
            model_name = available_models[0]
            model = genai.GenerativeModel(model_name)
            st.write(f"Використовується модель: {model_name}")
        else:
            st.error("Не знайдено жодної доступної моделі.")
            st.stop()
    except Exception as e:
        st.error(f"Помилка при пошуку моделей: {e}")
        st.stop()
else:
    st.error("GEMINI_API_KEY не знайдено в Secrets!")
    st.stop()

# Далі йде решта коду для чату...
st.title("Адмін-панель UKRAINE GTA")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Пароль:", type="password")
    if st.button("Увійти"):
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.authenticated = True
            st.rerun()
else:
    if prompt := st.chat_input("Питання:"):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Помилка ШІ: {e}")
