import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import io

def extract_data_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def create_xls(data):
    # Split the text into lines
    lines = data.split('\n')
    
    # Initialize an empty list to hold the rows of data
    rows = []
    
    # Iterate through each line
    for line in lines:
        # Split the line by commas (or any other delimiter used in the PDF)
        columns = line.split(',')
        
        # Append the columns to the rows list
        rows.append(columns)
    
    # Convert the list of rows into a DataFrame
    df = pd.DataFrame(rows)
    
    return df

def main():
    st.title('PDF to XLS Converter')
    
    # File upload
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    
    if uploaded_file is not None:
        # Extract data from the uploaded PDF file
        pdf_data = extract_data_from_pdf(io.BytesIO(uploaded_file.read()))
        
        # Create XLS file with predefined columns
        df = create_xls(pdf_data)
        
        # Display DataFrame
        st.write("Data extracted from PDF:")
        st.write(df)
        
        # Download XLS file
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        st.download_button(
            label="Download XLS",
            data=excel_buffer,
            file_name='output.xls',
            mime='application/vnd.ms-excel'
        )

if __name__ == '__main__':
    main()