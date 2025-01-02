import spacy
from spacy.matcher import Matcher
# import re
import pattern_analyzer
import streamlit as st
# import sys
# from risk_analyzer import analyze_text_for_risks
from document_extractor import extract_text_from_docx, extract_text_from_pdf


nlp = spacy.load("en_core_web_sm")

matcher_nlp = Matcher(nlp.vocab)

# def analyze_text_for_risks(text):
#     doc = nlp(text)
#     risks = []
#     matcher = pattern_analyzer.add_risk_patterns(matcher_nlp)
#     matches = matcher(doc)

#     for match_id, start, end in matches:
#         string_id = nlp.vocab.strings[match_id]
#         span = doc[start:end]
#         risks.append({"risk": string_id, "matched_text": span.text})

#     return risks

def analyze_text_for_risks(text):
    doc = nlp(text)
    risks = []
    matcher = pattern_analyzer.add_risk_patterns(matcher_nlp)
    matches = matcher(doc)

    # Define risk weights
    risk_weights = {
        "SCOPE_CREEP_BASIC": 4,  # Higher weight for explicit "scope creep"
        "SCOPE_CREEP_CONTEXTUAL": 3, # Slightly lower weight for less explicit scope creep
        "SCHEDULE_DELAY": 5,      # High weight for schedule delays
        "BUDGET_OVERRUN": 5,     # High weight for budget overruns
        "RESOURCE_SHORTAGE": 3,  # Medium weight for resource shortages
        "TECHNICAL_DIFFICULTY": 2, # Lower weight for technical difficulties (can vary)
    }


    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]
        weight = risk_weights.get(string_id, 1)  # Get the weight or default to 1
        # print('\n \n span: ', span.text.lower())
        # if string_id == "SCHEDULE_DELAY":
        #     if "significant" in span.text.lower() or "major" in span.text.lower():
        #         weight *= 2  # Double the weight for significant delays
        #         print('\n weight ', weight)
                # score = weight # update the score
                # risks.append({
                #     "risk": string_id,
                #     "matched_text": span.text,
                #     "weight": weight,
                #     "score": score
                # })
        risks.append({
            "risk": string_id,
            "matched_text": span.text,
            "weight": weight,
            "score": weight # Initialize score to weight
        })

    return risks

# Example Usage
# text = "There have been significant technical difficulties that have caused a delay in the project. The budget has exceeded projections. There is a lack of resources. We are adding a new feature. There will be a change to the requirement. We will add on to the requirements. There is scope creep."
# risks = analyze_text_for_risks(text)
# print(risks)

# Example to show how to sum up the risks
def calculate_total_risk_score(risks):
    total_score = 0
    for risk in risks:
        total_score += risk["score"]
    return total_score



def app():
    st.title("Project Risk Analyzer")

    uploaded_file = st.file_uploader("Upload a project document (docx, pdf, or txt)", type=["docx", "pdf", "txt"])

    if uploaded_file is not None:
        try:
            file_name = uploaded_file.name
            if "." not in file_name: # Check if there is an extension
                st.error("Uploaded file must have an extension (e.g., .docx, .pdf, .txt).")
                st.stop()
            file_extension = file_name.split(".")[-1].lower()
            file_content = uploaded_file.read()
            text = None

            with st.spinner("Processing document..."):
                if file_extension == "docx":
                    text = extract_text_from_docx(uploaded_file)
                elif file_extension == "pdf":
                    text = extract_text_from_pdf(uploaded_file)
                elif file_extension == "txt":
                    text = file_content.decode("utf-8", errors="ignore")
                else:
                    st.error("Unsupported file format.")
                    st.stop()

            if text:
                st.write("Extracted Text:")
                st.write(text)
                risks = analyze_text_for_risks(text)

                if risks:
                    st.subheader("Detected Risks:")
                    total_risk = calculate_total_risk_score(risks)
                    st.write(f"Total risk score: {total_risk}")
                    for risk in risks:
                        st.write(f"- **{risk['risk']}**: {risk['matched_text']} (Weight: {risk['weight']}, Score: {risk['score']})")
                else:
                    st.write("No risks detected in the document.")
            else:
                st.error("Could not extract text from the file. Please check the file format and content.")

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}") # More general error message
            st.stop()
    else:
        st.write("Please upload a file to analyze.")

        
# st.title("Project Risk Analyzer")

# uploaded_file = st.file_uploader("Upload a project document (docx, pdf, or txt)", type=["docx", "pdf", "txt"])
# print('\n uploaded FILE: ', uploaded_file)
# if uploaded_file is not None:
#     file_extension = uploaded_file.name.split(".")[-1].lower()
#     file_content = uploaded_file.read()
#     text = None # initialize text
#     print('\n IF uploaded FILE')

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




# total_risk = calculate_total_risk_score(risks)
# print(f"Total risk score: {total_risk}")
# def analyze_text_for_risks(text):
#     doc = nlp(text)
#     risks = []

#     # 1. Schedule Delays
#     schedule_keywords = ["behind schedule", "delayed", "postponed", "deadline missed", "deadline has been pushed back", "slippage", "overdue"]
#     for keyword in schedule_keywords:
#         if keyword in text.lower():  # Case-insensitive matching
#             risks.append({"risk": "Schedule Delay", "keyword": keyword})

#     # Regex for date delays (example - needs refinement)
#     date_delay_regex = r"delayed until (\d{2}/\d{2}/\d{4})" # example: 12/24/2024
#     date_matches = re.findall(date_delay_regex, text)
#     if date_matches:
#         for match in date_matches:
#             risks.append({"risk": "Schedule Delay (Date)", "date": match})

#     # 2. Budget Overruns (Simplified)
#     budget_keywords = ["cost increase", "budget exceeded", "over budget", "cost overrun"]
#     for keyword in budget_keywords:
#         if keyword in text.lower():
#             risks.append({"risk": "Budget Overrun", "keyword": keyword})

#     # Regex for cost increases (example)
#     cost_increase_regex = r"cost increased by \$(\d+(?:\.\d{2})?)"
#     cost_matches = re.findall(cost_increase_regex, text)
#     if cost_matches:
#         for match in cost_matches:
#             risks.append({"risk": "Budget Overrun (Amount)", "amount": match})

#     # Add similar keyword checks and regexes for other risk factors
#     # ... (Scope Creep, Resource Shortages, Technical Difficulties)
    
#     # 3. Scope Creep
#     scope_keywords = ["scope creep", "additional requirements", "change requests", "new features", "expanded scope", "out of scope", "unplanned work", "feature creep", "requirement changes", "added features", "extra work", "modified requirements", "scope change"]
#     for keyword in scope_keywords:
#         if keyword in text.lower():  # Case-insensitive matching
#             risks.append({"risk": "Scope Creep", "keyword": keyword})

#     # 4. Resource Shortages
#     resource_keywords = ["lack of resources", "resource constraints", "staff shortage", "equipment unavailability", "material delays", "resource allocation issues", "limited resources", "not enough manpower", "insufficient staff", "lack of personnel"]  
#     for keyword in resource_keywords:
#         if keyword in text.lower():  # Case-insensitive matching
#             risks.append({"risk": "Resource Shortages", "keyword": keyword})

#     # 5. Technical Difficulties
#     technical_difficulties_keywords = ["technical difficulties", "integration problems", "software bugs", "hardware failures", "compatibility issues", "system errors", "technical challenges", "implementation issues", "debugging", "testing issues", "system downtime", "performance issues", "software defects", "hardware malfunction"]
#     for keyword in technical_difficulties_keywords:
#         if keyword in text.lower():  # Case-insensitive matching
#             risks.append({"risk": "Technical Difficulties", "keyword": keyword})


#     return risks



# Example Usage:
# text1 = "The project is now behind schedule due to unforeseen circumstances. The cost increased by $5000."
# text2 = "We have received several change requests that could lead to scope creep. We have a lack of resources to handle this."
# text3 = "The meeting minutes show that the deadline has been pushed back to 10/26/2024. This is due to software bugs."

# risks1 = analyze_text_for_risks(text1)
# risks2 = analyze_text_for_risks(text2)
# risks3 = analyze_text_for_risks(text3)

# print("Risks in text1:", risks1)
# print("Risks in text2:", risks2)
# print("Risks in text3:", risks3)