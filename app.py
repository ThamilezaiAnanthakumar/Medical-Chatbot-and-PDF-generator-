import streamlit as st
from fpdf import FPDF
import openai

# Set OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Initialize Streamlit app
st.title('Medical Chatbot and PDF Generator')

# User input
st.header('Medical Chatbot')
user_input = st.text_area('Describe your symptoms or ask a medical question:')

# Chatbot response
if st.button('Get Response'):
    if user_input:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=f"You are a medical assistant. Answer the following: {user_input}",
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()
        st.text_area('Chatbot Response:', value=bot_response, height=200)
    else:
        st.warning('Please enter a question or description.')

# PDF Generation
st.header('Generate PDF Report')
patient_name = st.text_input('Patient Name:')
age = st.text_input('Age:')
diagnosis = st.text_area('Diagnosis:')
treatment = st.text_area('Treatment Plan:')

if st.button('Generate PDF'):
    if patient_name and age and diagnosis and treatment:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Medical Report', ln=True, align='C')
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, f"Patient Name: {patient_name}")
        pdf.multi_cell(0, 10, f"Age: {age}")
        pdf.multi_cell(0, 10, f"Diagnosis: {diagnosis}")
        pdf.multi_cell(0, 10, f"Treatment Plan: {treatment}")
        pdf_output_path = 'medical_report.pdf'
        pdf.output(pdf_output_path)
        st.success('PDF Generated Successfully!')
        with open(pdf_output_path, 'rb') as f:
            st.download_button('Download PDF', f, file_name=pdf_output_path, mime='application/pdf')
    else:
        st.warning('Please fill out all fields before generating PDF.')
