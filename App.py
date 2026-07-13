import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="AI Language Translator", page_icon="🌐", layout="centered")

st.title("🌐 AI Language Translation Tool")
st.write("Enter your text, select the target language, and get instant translations!")


LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Telugu": "te",
    "Malayalam": "ml",
    "Kannada": "kn"
}


col1, col2 = st.columns(2)

with col1:
    src_lang = st.selectbox("Source Language", ["Auto Detect"] + list(LANGUAGES.keys()))

with col2:
    target_lang = st.selectbox("Target Language", list(LANGUAGES.keys()), index=1) # Defaults to Hindi


text_to_translate = st.text_area("Enter Text to Translate", placeholder="Type something here...", height=150)


if st.button("Translate Text", use_container_width=True):
    if text_to_translate.strip() == "":
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
               
                src_code = "auto" if src_lang == "Auto Detect" else LANGUAGES[src_lang]
                target_code = LANGUAGES[target_lang]
                
            
                translated = GoogleTranslator(source=src_code, target=target_code).translate(text_to_translate)
                
              
                st.success("Translation Complete!")
                st.text_area("Translated Output", value=translated, height=150, disabled=False)
                
            except Exception as e:
                st.error(f"An error occurred during translation: {e}")


st.markdown("---")
st.caption("CodeAlpha AI Internship - Task 1 | Built with Streamlit & Deep-Translator")