import streamlit as st
from inference.generate import generate_answer

st.title("🧠 CONFIDENCE-GPT")
st.write("A self-aware LLM that answers only when confident")

query = st.text_input("Enter your question")

if query:
    result = generate_answer(query)
    st.write("You asked:", result["question"])
    st.write("Answer:")
    st.info(result["answer"])
    st.write("Confidence Score:", round(result["confidence"], 2))
    st.write("Verdict:", result["verdict"])
