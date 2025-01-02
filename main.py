# main.py
import sys # for command line arguments
from risk_analyzer import app
from document_extractor import extract_text_from_docx, extract_text_from_pdf
import streamlit as st

if __name__ == "__main__":
    app()
    # print("\n python main.py <file_path>", sys.argv)
    # if len(sys.argv) != 2: # Check if a file path is provided
    #     print("Usage: python main.py <file_path>")
    #     sys.exit(1)

    # file_path = sys.argv[1]
    # file_path = 'my_project_plan.docx'
    # print("\n file_path test", file_path) 
    # file_extension = file_path.split(".")[-1].lower()

    # if file_extension == "docx":
    #     text = extract_text_from_docx(file_path)
    #     # print('\n docx file', file_path, text)
    # elif file_extension == "pdf":
    #     text = extract_text_from_pdf(file_path)
    # elif file_extension == "txt":
    #     try:
    #         with open(file_path, "r", encoding="utf-8") as file:
    #             text = file.read()
    #     except FileNotFoundError:
    #         print(f"Error: File not found at {file_path}")
    #         sys.exit(1)
    # else:
    #     print("Unsupported file format. Please provide a .docx, .pdf, or .txt file.")
    #     sys.exit(1)


    # st.title("Project Risk Analyzer")

    # uploaded_file = st.file_uploader("Upload a project document (docx, pdf, or txt)", type=["docx", "pdf", "txt"])
    # print('\n uploaded FILE: ', uploaded_file)
    # if uploaded_file is not None:
    #     file_extension = uploaded_file.name.split(".")[-1].lower()
    #     file_content = uploaded_file.read()
    #     text = None # initialize text
    # try:
    #     if file_extension == "docx":
    #         text = extract_text_from_docx(uploaded_file)
    #     elif file_extension == "pdf":
    #         text = extract_text_from_pdf(uploaded_file)
    #     elif file_extension == "txt":
    #         text = file_content.decode("utf-8", errors = "ignore") # decode bytes to string, ignore errors
    #     else:
    #         st.error("Unsupported file format.")
    #         st.stop()
    # except Exception as e:
    #     st.error(f"Error processing the file: {e}")
    #     st.stop()
    
    # if text:
    #     st.write("Extracted Text:") # Debugging: Print extracted text
    #     st.write(text) # Debugging: Print extracted text
    #     risks = analyze_text_for_risks(text)
    #     print('\n frontend RISKS ', risks)
    #     if risks:
    #         st.subheader("Detected Risks:")
    #         total_risk = calculate_total_risk_score(risks)
    #         st.write(f"Total risk score: {total_risk}")
    #         for risk in risks:
    #             st.write(f"- **{risk['risk']}**: {risk['matched_text']} (Weight: {risk['weight']}, Score: {risk['score']})")

    #     else:
    #         st.write("No risks detected in the document.")
    # else:
    #     st.error("Could not extract text from the file.")


    # if text: # Only analyze if text extraction was successful
    #     risks = analyze_text_for_risks(text)
    #     print(f"\n Risks found in {file_path}:", risks)
    #     total_risk = calculate_total_risk_score(risks)
    #     print(f"\n Total risk score: {total_risk}")
    # else:
    #     print("\n No text could be extracted from the file.", text, file_path)
    #     print("\n Test function", analyze_text_for_risks(text))
    #     print('\n failure error')
    #     sys.exit(1)


