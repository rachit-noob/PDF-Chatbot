import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
import torch

# PDF Processing
def extract_text_from_pdf(uploaded_file):
  text = ""
  try:
    pdf_content = uploaded_file.read()  # Read the uploaded file content
    pdf_document = fitz.open(stream=pdf_content)  # Open the PDF from content
    for page in pdf_document:
      text += page.get_text()
  except Exception as e:
    st.error(f"Error processing PDF: {e}")
  return text





# Question Answering Model
def question_answer(question, context):
    qa_model = pipeline("question-answering", model="deepset/bert-base-cased-squad2", tokenizer="deepset/bert-base-cased-squad2")
    result = qa_model(question=question, context=context)
    return result

# Streamlit UI
def main():
    st.title("PDF Chatbot")

    uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")

    if uploaded_files:
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            st.write(f"### Analyzing {file.name}")


            question = st.text_input("Ask a question about the text:")
            if st.button("Get Answer"):
                if question:
                    answer = question_answer(question, text)
                    st.write("Answer:", answer['answer'])
                else:
                    st.write("Please ask a question.")

if __name__ == "__main__":
    main()
