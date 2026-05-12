"""
Customer Data Chatbot using Streamlit
"""

import streamlit as st
import os
from data_loader import load_excel_data
from query_engine import create_query_engine

# Getting Gemini API key from environment variable
gemini_key = os.getenv("GEMINI_API_KEY")

# Streamlit page settings
st.set_page_config(
    page_title="Customer Data Assistant",
    page_icon="📊",
    layout="centered"
)

# Main heading
st.title("📊 Customer Data Assistant")
st.write("Upload your Excel file and ask questions in simple English.")

# Upload Excel file
excel_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"]
)

st.caption("Supported file types: .xlsx and .xls")

if excel_file is not None:

    # Loading Excel data
    customer_df = load_excel_data(excel_file)

    st.success("File uploaded successfully")

    # Showing sample data
    with st.expander("Preview Data"):
        st.dataframe(customer_df.head())

    # User question input
    st.subheader("Ask Your Question")

    user_question = st.text_input(
        "Enter your question here"
    )

    st.markdown("""
    ### Example Questions
    - How many customers have budget above 90 lakhs?
    - List customers looking for 2BHK in Pune
    - What is the average budget?
    """)

    # Button to process question
    if st.button("Get Answer"):

        if not gemini_key:
            st.error("Please set GEMINI_API_KEY")

        elif not user_question:
            st.warning("Please enter a question")

        else:

            with st.spinner("Getting answer..."):

                chatbot_engine = create_query_engine(
                    gemini_key,
                    customer_df
                )

                output = chatbot_engine.query(user_question)

            if output['success']:

                # Showing summary
                if output['summary']:
                    st.subheader("Summary")
                    st.write(output['summary'])

                # Showing final result
                if output['answer']:
                    st.subheader("Answer")
                    st.code(output['answer'])

            else:
                st.error(output['answer'])

else:
    st.info("Please upload an Excel file to continue")