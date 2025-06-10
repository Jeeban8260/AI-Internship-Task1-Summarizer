import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration
import time

st.set_page_config(page_title="Task 1 – Summarizer 💻", layout="wide")

st.markdown("<h1 style='text-align:center; color:#00ffff;'>CODTECH INTERNSHIP – TASK 1</h1>🧠", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    return tokenizer, model

tokenizer, model = load_model()

col1, col2 = st.columns(2)

default_article = (
    "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. "
    "These machines are designed to think and act like humans, and they can be trained to learn "
    "from experience and perform tasks such as problem-solving, speech recognition, decision-making, and language translation. "
    "AI has evolved rapidly over the last few decades and is now embedded in many areas of modern life, "
    "from personal assistants like Siri and Alexa to self-driving cars and healthcare diagnostics."
)

with col1:
    st.markdown("### Paste or Upload Article: 📄")
    uploaded_files = st.file_uploader("Upload .txt files", type=["txt"], accept_multiple_files=True)
    
    input_text = st.text_area("Write or paste article here:", default_article, height=300)

    if uploaded_files:
        for file in uploaded_files:
            file_content = file.read().decode("utf-8")
            input_text += "\n" + file_content
        uploaded_names = ", ".join([file.name for file in uploaded_files])
        st.info(f"Uploaded Files: {uploaded_names} 📂")

with col2:
    st.markdown("### Summary Output: 📌")
    summary_placeholder = st.empty()

    if st.button("Summarize ✨"):
        with st.spinner("Generating your sexy summary..."):
            input_ids = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = model.generate(
                input_ids,
                max_length=150,
                num_beams=4,
                no_repeat_ngram_size=3,
                repetition_penalty=2.5,
                length_penalty=1.5,
                early_stopping=True
            )
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

            animated = ""
            for ch in summary:
                animated += ch
                summary_placeholder.markdown(
                    f"<p style='color:#00ff88;font-size:18px;'>{animated}</p>",
                    unsafe_allow_html=True
                )
                time.sleep(0.01)